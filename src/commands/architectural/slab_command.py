"""SLAB 5.0.8.4 — creación y edición BIM estructural."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QInputDialog

from commands.base_command import BaseCommand
from core.history.add_slab_action import AddSlabAction
from core.history.edit_slab_action import EditSlabAction
from engines.architectural.room_detector import RoomDetector
from engines.architectural.room_engine import RoomEngine
from engines.architectural.slab_engine import SlabEngine
from engines.geometry.point import Point


class SlabCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "SLAB"

        self.thickness = 0.15
        self.material = "Concreto armado"
        self.elevation = 0.0

        self.concrete_strength_mpa = 25.0
        self.density_kg_m3 = 2400.0
        self.superimposed_dead_load_kg_m2 = 100.0
        self.live_load_kg_m2 = 200.0
        self.finish_load_kg_m2 = 50.0

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)
        if command_line is not None:
            command_line.set_prompt(text)
            command_line.focus_input()

    def _status(self, canvas, text):
        window = self._window(canvas)
        if window is not None:
            window.statusBar().showMessage(text)

    def _scene(self, canvas):
        return getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

    def _point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)
        if callable(getter):
            point = getter()
            if point is not None:
                return point
        x, y = getattr(canvas, "cursor_position", (0.0, 0.0))
        return Point(x, y, 0.0)

    def _room_at(self, scene, point):
        candidates = []
        for room in RoomEngine.scene_rooms(scene):
            boundary = list(getattr(room, "boundary", []) or [])
            if (
                getattr(room, "valid", False)
                and RoomDetector.point_in_polygon(point, boundary)
            ):
                candidates.append(room)

        if not candidates:
            return None
        return min(candidates, key=lambda room: room.area)

    def _push_history(self, action):
        history = getattr(self.app_core, "history", None)
        push = getattr(history, "push", None)
        if callable(push):
            push(action)

    def _get_double(
        self,
        parent,
        title,
        label,
        value,
        minimum=0.0,
        maximum=100000.0,
        decimals=3,
    ):
        return QInputDialog.getDouble(
            parent,
            title,
            label,
            float(value),
            minimum,
            maximum,
            decimals,
        )

    def _collect_data(self, canvas, current):
        parent = self._window(canvas)
        data = dict(current)

        data["thickness"], ok = self._get_double(
            parent,
            "Datos estructurales de losa",
            "Espesor de la losa (m):",
            data["thickness"],
            0.001,
            10.0,
            3,
        )
        if not ok:
            return None

        material, ok = QInputDialog.getText(
            parent,
            "Datos estructurales de losa",
            "Material:",
            text=str(data["material"]),
        )
        if not ok:
            return None
        data["material"] = material.strip() or "Concreto armado"

        data["elevation"], ok = self._get_double(
            parent,
            "Datos estructurales de losa",
            "Elevación (m):",
            data["elevation"],
            -10000.0,
            10000.0,
            3,
        )
        if not ok:
            return None

        data["concrete_strength_mpa"], ok = self._get_double(
            parent,
            "Datos estructurales de losa",
            "Resistencia del concreto f'c (MPa):",
            data["concrete_strength_mpa"],
            0.0,
            200.0,
            2,
        )
        if not ok:
            return None

        data["density_kg_m3"], ok = self._get_double(
            parent,
            "Datos estructurales de losa",
            "Densidad del material (kg/m³):",
            data["density_kg_m3"],
            0.0,
            10000.0,
            1,
        )
        if not ok:
            return None

        data["superimposed_dead_load_kg_m2"], ok = self._get_double(
            parent,
            "Cargas de losa",
            "Carga muerta adicional (kg/m²):",
            data["superimposed_dead_load_kg_m2"],
            0.0,
            100000.0,
            2,
        )
        if not ok:
            return None

        data["finish_load_kg_m2"], ok = self._get_double(
            parent,
            "Cargas de losa",
            "Carga de acabados (kg/m²):",
            data["finish_load_kg_m2"],
            0.0,
            100000.0,
            2,
        )
        if not ok:
            return None

        data["live_load_kg_m2"], ok = self._get_double(
            parent,
            "Cargas de losa",
            "Sobrecarga de uso (kg/m²):",
            data["live_load_kg_m2"],
            0.0,
            100000.0,
            2,
        )
        if not ok:
            return None

        return data

    def _default_snapshot(self):
        return {
            "thickness": self.thickness,
            "material": self.material,
            "elevation": self.elevation,
            "concrete_strength_mpa": self.concrete_strength_mpa,
            "density_kg_m3": self.density_kg_m3,
            "superimposed_dead_load_kg_m2": (
                self.superimposed_dead_load_kg_m2
            ),
            "finish_load_kg_m2": self.finish_load_kg_m2,
            "live_load_kg_m2": self.live_load_kg_m2,
        }

    def _save_defaults(self, data):
        self.thickness = data["thickness"]
        self.material = data["material"]
        self.elevation = data["elevation"]
        self.concrete_strength_mpa = (
            data["concrete_strength_mpa"]
        )
        self.density_kg_m3 = data["density_kg_m3"]
        self.superimposed_dead_load_kg_m2 = (
            data["superimposed_dead_load_kg_m2"]
        )
        self.finish_load_kg_m2 = data["finish_load_kg_m2"]
        self.live_load_kg_m2 = data["live_load_kg_m2"]

    def _edit_existing(self, slab, canvas):
        before = slab.data_snapshot()
        after = self._collect_data(canvas, before)

        if after is None:
            print("SLAB edición cancelada")
            return False

        slab.apply_data_snapshot(after)

        if after != before:
            self._push_history(
                EditSlabAction(
                    slab,
                    before,
                    after,
                )
            )

        print(
            f"SLAB actualizada: espesor={slab.thickness:g} m, "
            f"material={slab.material}, "
            f"f'c={slab.concrete_strength_mpa:g} MPa, "
            f"peso propio={slab.self_weight_kg_m2:.2f} kg/m², "
            f"carga muerta total="
            f"{slab.total_dead_load_kg_m2:.2f} kg/m², "
            f"sobrecarga={slab.live_load_kg_m2:.2f} kg/m², "
            f"carga servicio="
            f"{slab.total_service_load_kg_m2:.2f} kg/m², "
            f"volumen={slab.volume:g} m³"
        )
        self._status(
            canvas,
            f"SLAB | Servicio: "
            f"{slab.total_service_load_kg_m2:.1f} kg/m²",
        )
        canvas.update()
        return True

    def begin(self, canvas):
        print(
            f"SLAB activado: espesor={self.thickness:g} m, "
            f"material={self.material}, "
            f"f'c={self.concrete_strength_mpa:g} MPa"
        )
        self._prompt(
            canvas,
            "Seleccione ROOM. Clic en losa existente = editar datos estructurales:",
        )
        self._status(
            canvas,
            "SLAB: clic en ROOM nuevo para crear; existente para editar",
        )

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip().upper()

        if value in ("P", "PARAMETROS", "PARÁMETROS", "DATOS"):
            data = self._collect_data(
                canvas,
                self._default_snapshot(),
            )
            if data is not None:
                self._save_defaults(data)
                print(
                    f"SLAB parámetros nuevos: "
                    f"espesor={self.thickness:g} m, "
                    f"material={self.material}, "
                    f"f'c={self.concrete_strength_mpa:g} MPa"
                )
            return True

        return False

    def mouse_press(self, event, canvas):
        if event.button() != Qt.LeftButton:
            return

        scene = self._scene(canvas)
        room = self._room_at(scene, self._point(canvas))

        if room is None:
            print("SLAB: no se encontró un ROOM bajo el cursor")
            self._status(canvas, "SLAB: seleccione un ROOM válido")
            return

        existing = SlabEngine.find_by_room(scene, room)

        if existing is not None:
            print(
                f"SLAB seleccionada para editar: {existing.name}, "
                f"espesor={existing.thickness:g} m, "
                f"material={existing.material}, "
                f"volumen={existing.volume:g} m³"
            )
            self._edit_existing(existing, canvas)
            return

        data = self._collect_data(
            canvas,
            self._default_snapshot(),
        )
        if data is None:
            print("SLAB creación cancelada")
            return

        self._save_defaults(data)

        slab = SlabEngine.create_from_room(
            room,
            thickness=self.thickness,
            material=self.material,
            elevation=self.elevation,
        )

        slab.set_concrete_strength(
            self.concrete_strength_mpa
        )
        slab.set_density(self.density_kg_m3)
        slab.set_superimposed_dead_load(
            self.superimposed_dead_load_kg_m2
        )
        slab.set_finish_load(self.finish_load_kg_m2)
        slab.set_live_load(self.live_load_kg_m2)

        result = SlabEngine.add_to_scene(scene, slab)

        if not result:
            print("SLAB: no se pudo agregar la losa")
            return

        self._push_history(AddSlabAction(scene, slab))

        print(
            f"SLAB creada: ambiente={room.name}, "
            f"área={slab.area:g} m², "
            f"espesor={slab.thickness:g} m, "
            f"volumen={slab.volume:g} m³, "
            f"material={slab.material}, "
            f"f'c={slab.concrete_strength_mpa:g} MPa, "
            f"carga servicio="
            f"{slab.total_service_load_kg_m2:.2f} kg/m²"
        )
        self._status(
            canvas,
            f"SLAB: {slab.area:.2f} m² | "
            f"{slab.total_service_load_kg_m2:.1f} kg/m²",
        )
        self._prompt(
            canvas,
            "Seleccione otro ROOM o pulse ESC:",
        )
        canvas.update()

    def key_press(self, event, canvas):
        if event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        if canvas is not None:
            self._prompt(canvas, "Comando:")
            self._status(canvas, "SLAB cancelado")
            canvas.update()
        print("SLAB cancelado")

    def deactivate(self):
        print("SLAB desactivado")
