"""Comando ROOM 5.0.7.3 — detección automática."""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_room_action import AddRoomAction
from engines.architectural.room_engine import RoomEngine
from engines.geometry.point import Point


class RoomCommand(BaseCommand):
    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "ROOM"

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

        position = getattr(canvas, "cursor_position", (0.0, 0.0))
        return Point(position[0], position[1], 0.0)

    def begin(self, canvas):
        print("ROOM activado: detección automática 5.0.7.3")
        self._prompt(canvas, "Seleccione un punto interior del recinto:")
        self._status(canvas, "ROOM: haga clic dentro de un recinto cerrado")

    def mouse_press(self, event, canvas):
        scene = self._scene(canvas)
        if scene is None:
            self._status(canvas, "ROOM: no hay una escena activa")
            return

        point = self._point(canvas)
        room = RoomEngine.create_room(scene, point)

        if room is None:
            print("ROOM: no se detectó un recinto cerrado bajo el cursor")
            self._status(
                canvas,
                "ROOM: el punto no pertenece a un recinto cerrado",
            )
            return

        existing = RoomEngine.equivalent_room(
            scene,
            room.boundary_key,
        )
        if existing is not None:
            print(
                f"ROOM existente: {existing.name}, "
                f"área={existing.area:g} m²"
            )
            self._status(canvas, "ROOM: este recinto ya fue creado")
            return

        RoomEngine.add_to_scene(scene, room)

        if self.app_core is not None:
            self.app_core.history.push(
                AddRoomAction(scene, room)
            )

        print(
            f"ROOM creado: {room.name}, "
            f"área={room.area:g} m², "
            f"perímetro={room.perimeter:g} m"
        )
        self._status(
            canvas,
            f"{room.name}: {room.area:.2f} m²",
        )
        self._prompt(
            canvas,
            "Seleccione otro recinto o pulse ESC:",
        )
        canvas.update()

    def key_press(self, event, canvas):
        if event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        if canvas is not None:
            self._prompt(canvas, "Comando:")
            self._status(canvas, "ROOM cancelado")
        print("ROOM cancelado")

    def deactivate(self):
        print("ROOM desactivado")
