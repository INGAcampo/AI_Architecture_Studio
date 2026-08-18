"""ROOMEDIT 5.0.7.4 — edición de datos BIM."""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.edit_room_action import EditRoomAction
from engines.architectural.room_detector import RoomDetector
from engines.architectural.room_engine import RoomEngine
from engines.geometry.point import Point


class RoomEditCommand(BaseCommand):
    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "ROOMEDIT"
        self.room = None
        self.awaiting = None
        self.before = None

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
            return getter()
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

    def begin(self, canvas):
        self.room = None
        self.awaiting = None
        print("ROOMEDIT activado")
        self._prompt(canvas, "Seleccione un ROOM:")
        self._status(canvas, "ROOMEDIT: seleccione una habitación")

    def mouse_press(self, event, canvas):
        if event.button() != Qt.LeftButton:
            return
        room = self._room_at(self._scene(canvas), self._point(canvas))
        if room is None:
            self._status(canvas, "ROOMEDIT: no se encontró ROOM")
            return
        self.room = room
        self.before = room.data_snapshot()
        canvas.highlight.set(room)
        canvas.update()
        print(
            f"ROOM seleccionado: {room.name}, "
            f"{room.area:.2f} m², {room.category_label}"
        )
        self._prompt(
            canvas,
            "[N=Nombre / T=Tipo / NUM=Número / C=Comentarios / ENTER=Finalizar]:",
        )

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()
        upper = value.upper()

        if self.room is None:
            return False

        if self.awaiting is not None:
            if self.awaiting == "name":
                self.room.set_name(value)
            elif self.awaiting == "category":
                self.room.set_category(value)
            elif self.awaiting == "number":
                self.room.set_number(value)
            elif self.awaiting == "comments":
                self.room.set_comments(value)
            self.awaiting = None
            canvas.update()
            self._prompt(
                canvas,
                "[N=Nombre / T=Tipo / NUM=Número / C=Comentarios / ENTER=Finalizar]:",
            )
            return True

        if upper in ("N", "NOMBRE"):
            self.awaiting = "name"
            self._prompt(canvas, "Nuevo nombre:")
            return True

        if upper in ("T", "TIPO", "CATEGORIA", "CATEGORÍA"):
            self.awaiting = "category"
            self._prompt(
                canvas,
                "Tipo [General/Sala/Dormitorio/Cocina/Baño/Servicio/Pasillo/Exterior]:",
            )
            return True

        if upper in ("NUM", "NUMERO", "NÚMERO"):
            self.awaiting = "number"
            self._prompt(canvas, "Número de ambiente:")
            return True

        if upper in ("C", "COMENTARIO", "COMENTARIOS"):
            self.awaiting = "comments"
            self._prompt(canvas, "Comentarios:")
            return True

        if upper in ("ENTER", "FINALIZAR", "OK"):
            self.finish(canvas)
            return True

        return False

    def finish(self, canvas):
        if self.room is None:
            return

        after = self.room.data_snapshot()
        if after != self.before:
            history = getattr(self.app_core, "history", None)
            push = getattr(history, "push", None)
            if callable(push):
                push(EditRoomAction(self.room, self.before, after))

        print(
            f"ROOM actualizado: {self.room.name}, "
            f"tipo={self.room.category_label}, "
            f"número={self.room.number or '-'}"
        )
        canvas.highlight.clear()
        canvas.update()
        self.room = None
        self.before = None
        self._prompt(canvas, "Seleccione otro ROOM o pulse ESC:")

    def key_press(self, event, canvas):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.finish(canvas)
        elif event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        if self.room is not None and self.before is not None:
            self.room.apply_data_snapshot(self.before)
        self.room = None
        self.before = None
        self.awaiting = None
        if canvas is not None:
            canvas.highlight.clear()
            canvas.update()
        print("ROOMEDIT cancelado")

    def deactivate(self):
        print("ROOMEDIT desactivado")
