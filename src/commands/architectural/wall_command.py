"""
AI Architecture Studio
Architectural WALL Command

Architectural Core 5.0.4.1 — WALL Visual Professional
"""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.architectural.wall_engine import WallEngine
from engines.architectural.wall_network import WallNetwork
from engines.geometry.point import Point


class WallCommand(BaseCommand):

    MIN_SEGMENT_LENGTH = 1.0e-6

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "WALL"
        self.thickness = WallEngine.DEFAULT_THICKNESS
        self.justification = "center"
        self.points = []
        self.first_point = None
        self.awaiting_thickness = False

    # ---------------------------------------------------------
    # UI Y SERVICIOS
    # ---------------------------------------------------------

    def _window(self, canvas):
        getter = getattr(canvas, "window", None)
        return getter() if callable(getter) else None

    def _status(self, canvas, text):
        window = self._window(canvas)
        if window is not None:
            window.statusBar().showMessage(text)

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)
        if command_line is not None:
            command_line.set_prompt(text)

    def _focus_command_line(self, canvas):
        window = self._window(canvas)
        command_line = getattr(window, "command_line", None)
        if command_line is not None:
            command_line.focus_input()

    def _scene(self, canvas):
        return getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

    def _canvas_point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)
        if callable(getter):
            return getter()

        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def _apply_ortho(self, canvas, point):
        if self.first_point is None:
            return point

        getter = getattr(canvas, "get_ortho_manager", None)
        ortho = getter() if callable(getter) else None

        if ortho is None:
            return point

        return ortho.apply(self.first_point, point)

    # ---------------------------------------------------------
    # CICLO DEL COMANDO
    # ---------------------------------------------------------

    def activate(self):
        super().activate()
        print(
            f"WALL activado: espesor={self.thickness:g} m"
        )

    def begin(self, canvas):
        self._prompt(
            canvas,
            f"Primer punto del muro "
            f"[Espesor={self.thickness:g}]:",
        )
        self._status(
            canvas,
            "WALL activo: especifica el primer punto",
        )
        self._focus_command_line(canvas)

    def mouse_press(self, event, canvas):
        point = self._apply_ortho(
            canvas,
            self._canvas_point(canvas),
        )
        self.accept_point(point, canvas)

    def mouse_move(self, event, canvas):
        if not self.points:
            canvas.preview_geometry = None
            return

        point = self._apply_ortho(
            canvas,
            self._canvas_point(canvas),
        )

        canvas.preview_geometry = (
            WallEngine.create_preview(
                self.points,
                point,
                thickness=self.thickness,
                justification=self.justification,
            )
        )
        canvas.update()

    def accept_point(self, point, canvas):
        if self.points:
            previous = self.points[-1]

            if previous.distance_to(point) <= self.MIN_SEGMENT_LENGTH:
                self._status(
                    canvas,
                    "WALL: el nuevo punto debe ser distinto",
                )
                return False

        self.points.append(point)
        self.first_point = point

        print(
            f"WALL: Punto {len(self.points)} {point}"
        )

        if len(self.points) == 1:
            self._prompt(
                canvas,
                "Siguiente punto o E para espesor:",
            )
        else:
            self._prompt(
                canvas,
                "Siguiente punto o ENTER para finalizar:",
            )

        self._status(
            canvas,
            f"WALL: {max(0, len(self.points) - 1)} "
            "segmento(s) definidos",
        )
        self._focus_command_line(canvas)
        canvas.update()
        return True

    def finish(self, canvas):
        if len(self.points) < 2:
            self._status(
                canvas,
                "WALL: se requieren al menos dos puntos",
            )
            return False

        wall = WallEngine.create_wall(
            self.points,
            thickness=self.thickness,
            justification=self.justification,
        )

        scene = self._scene(canvas)
        if scene is None:
            self._status(
                canvas,
                "WALL: no hay una escena activa",
            )
            return False

        scene.add_element(wall)

        # WALL NETWORK 5.0.4.3: reconstruye y persiste la topología
        # de todos los muros presentes en la escena.
        network = WallNetwork.ensure_scene(scene)
        network_summary = network.summary()

        if self.app_core is not None:
            self.app_core.history.push(
                AddAction(scene, wall)
            )

        print(
            f"WALL creado: {wall.segment_count} segmento(s), "
            f"longitud={wall.length:g} m, "
            f"espesor={wall.thickness:g} m"
        )
        print(
            "WALL NETWORK: "
            f"nodos={network_summary['nodes']}, "
            f"L={network_summary['L']}, "
            f"T={network_summary['T']}, "
            f"X={network_summary['X']}"
        )

        self.points = []
        self.first_point = None
        self.awaiting_thickness = False

        canvas.preview_geometry = None
        canvas.current_snap_point = None
        canvas.current_snap_type = None
        canvas.highlight.clear()
        canvas.selection_manager.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self._status(
            canvas,
            "WALL creado. Especifica el primer punto "
            "del siguiente muro",
        )
        self._prompt(
            canvas,
            f"Primer punto del muro "
            f"[Espesor={self.thickness:g}]:",
        )
        self._focus_command_line(canvas)
        return True

    # ---------------------------------------------------------
    # TEXTO Y DYNAMIC INPUT
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if not value:
            return False

        upper = value.upper()

        if upper in {
            "E",
            "T",
            "ESPESOR",
            "THICKNESS",
        }:
            self.awaiting_thickness = True
            self._prompt(
                canvas,
                "Especifique espesor del muro:",
            )
            return True

        if upper in {
            "ENTER",
            "FIN",
            "FINALIZAR",
        }:
            return self.finish(canvas)

        if self.awaiting_thickness:
            try:
                thickness = float(
                    value.replace(",", ".")
                )
            except ValueError:
                self._status(
                    canvas,
                    "WALL: espesor no válido",
                )
                return True

            if thickness <= 0.0:
                self._status(
                    canvas,
                    "WALL: el espesor debe ser mayor que cero",
                )
                return True

            self.thickness = thickness
            self.awaiting_thickness = False

            print(
                f"WALL: espesor={self.thickness:g} m"
            )

            self._prompt(
                canvas,
                "Siguiente punto:"
                if self.points
                else "Primer punto del muro:",
            )
            self._status(
                canvas,
                f"WALL: espesor={self.thickness:g} m",
            )

            if self.points:
                canvas.preview_geometry = None

            canvas.update()
            return True

        try:
            point = CoordinateParser.parse(
                value,
                base_point=self.first_point,
            )
        except CoordinateParseError as error:
            self._status(
                canvas,
                f"WALL: {error}",
            )
            return False

        point = self._apply_ortho(canvas, point)
        return self.accept_point(point, canvas)

    def dynamic_input_value(self, manager):
        distance = manager.distance_field.value
        angle = manager.angle_field.value

        if not distance:
            return None

        if angle:
            return f"{distance}<{angle}"

        return str(distance)

    def key_press(self, event, canvas):
        if event.key() in (
            Qt.Key_Return,
            Qt.Key_Enter,
        ):
            self.finish(canvas)
            return

    def cancel(self, canvas=None):
        self.points = []
        self.first_point = None
        self.awaiting_thickness = False

        if canvas is not None:
            canvas.preview_geometry = None
            canvas.highlight.clear()
            canvas.update()
            self._prompt(canvas, "Comando:")
            self._status(canvas, "WALL cancelado")

        print("WALL cancelado")

    def deactivate(self):
        self.points = []
        self.first_point = None
        self.awaiting_thickness = False
        print("WALL desactivado")
