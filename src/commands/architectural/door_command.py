"""Comando DOOR — Architectural Core 5.0.5.2.1."""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_door_action import (
    AddDoorAction,
)
from engines.architectural.door_engine import (
    DoorEngine,
)
from engines.architectural.opening_engine import (
    OpeningEngine,
)
from engines.geometry.point import Point
from models.architectural.door import Door


class DoorCommand(BaseCommand):
    PICK_TOLERANCE = 0.75

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "DOOR"
        self.width = DoorEngine.DEFAULT_WIDTH
        self.height = DoorEngine.DEFAULT_HEIGHT
        self.handedness = Door.LEFT
        self.swing_direction = Door.INWARD

        self.selected_wall = None
        self.awaiting_property = None

    def _window(self, canvas):
        getter = getattr(
            canvas,
            "window",
            None,
        )
        return (
            getter()
            if callable(getter)
            else None
        )

    def _status(self, canvas, text):
        window = self._window(canvas)

        if window is not None:
            window.statusBar().showMessage(
                text
            )

    def _prompt(self, canvas, text):
        window = self._window(canvas)
        command_line = getattr(
            window,
            "command_line",
            None,
        )

        if command_line is not None:
            command_line.set_prompt(text)
            command_line.focus_input()

    def _scene(self, canvas):
        return getattr(
            self.app_core,
            "scene",
            getattr(
                canvas,
                "scene",
                None,
            ),
        )

    def _point(self, canvas):
        getter = getattr(
            canvas,
            "get_input_point",
            None,
        )

        if callable(getter):
            return getter()

        x, y = canvas.cursor_position
        return Point(
            x,
            y,
            0.0,
        )

    def _walls(self, scene):
        getter = getattr(
            scene,
            "get_elements",
            None,
        )
        elements = (
            getter()
            if callable(getter)
            else []
        )

        return [
            element
            for element in elements
            if element.__class__.__name__
            == "Wall"
            and getattr(
                element,
                "visible",
                True,
            )
        ]

    def _configuration_text(self):
        hand = (
            "IZQ"
            if self.handedness == Door.LEFT
            else "DER"
        )
        direction = (
            "INT"
            if self.swing_direction
            == Door.INWARD
            else "EXT"
        )

        return (
            f"A={self.width:g}, "
            f"H={self.height:g}, "
            f"{hand}, {direction}"
        )

    def begin(self, canvas):
        self.selected_wall = None
        self.awaiting_property = None

        print(
            "DOOR activado: "
            + self._configuration_text()
        )

        self._prompt(
            canvas,
            "Seleccione muro "
            f"[{self._configuration_text()}]:",
        )
        self._status(
            canvas,
            "DOOR activo: seleccione el muro anfitrión",
        )

    def mouse_press(
        self,
        event,
        canvas,
    ):
        scene = self._scene(canvas)
        point = self._point(canvas)

        if scene is None:
            self._status(
                canvas,
                "DOOR: no hay una escena activa",
            )
            return

        if self.selected_wall is None:
            result = OpeningEngine.nearest_wall(
                self._walls(scene),
                point,
                tolerance=self.PICK_TOLERANCE,
            )

            if result is None:
                self._status(
                    canvas,
                    "DOOR: no se encontró un muro cercano",
                )
                return

            self.selected_wall = result["wall"]
            canvas.highlight.set(
                self.selected_wall
            )
            canvas.update()

            self._prompt(
                canvas,
                "Indique el centro de la puerta sobre el muro:",
            )
            self._status(
                canvas,
                "DOOR: muro seleccionado; indique la posición",
            )
            return

        door = DoorEngine.create_door(
            self.selected_wall,
            point,
            width=self.width,
            height=self.height,
            handedness=self.handedness,
            swing_direction=self.swing_direction,
        )

        DoorEngine.add_to_wall(
            self.selected_wall,
            door,
        )

        if self.app_core is not None:
            self.app_core.history.push(
                AddDoorAction(
                    scene,
                    self.selected_wall,
                    door,
                )
            )

        scene.wall_network_signature = None

        print(
            "DOOR creado: "
            f"ancho={door.width:g} m, "
            f"altura={door.height:g} m, "
            f"mano={door.handedness}, "
            f"apertura={door.swing_direction}"
        )

        self.selected_wall = None
        canvas.highlight.clear()
        canvas.update()

        self._prompt(
            canvas,
            "Seleccione muro "
            f"[{self._configuration_text()}]:",
        )
        self._status(
            canvas,
            "DOOR creado. Seleccione otro muro o pulse ESC",
        )

    def _set_numeric(
        self,
        value,
        canvas,
    ):
        try:
            number = float(
                str(value).replace(
                    ",",
                    ".",
                )
            )
        except ValueError:
            self._status(
                canvas,
                "DOOR: valor numérico no válido",
            )
            return True

        if number <= 0.0:
            self._status(
                canvas,
                "DOOR: el valor debe ser mayor que cero",
            )
            return True

        if self.awaiting_property == "width":
            self.width = number
            label = "ancho"
        else:
            self.height = number
            label = "altura"

        self.awaiting_property = None

        self._status(
            canvas,
            f"DOOR: {label}={number:g} m",
        )
        self._prompt(
            canvas,
            (
                "Indique el centro de la puerta:"
                if self.selected_wall is not None
                else "Seleccione muro:"
            ),
        )
        return True

    def handle_text_input(
        self,
        text,
        canvas,
    ):
        value = str(
            text or ""
        ).strip()

        if not value:
            return False

        if self.awaiting_property is not None:
            return self._set_numeric(
                value,
                canvas,
            )

        upper = value.upper()

        if upper in (
            "A",
            "ANCHO",
            "WIDTH",
        ):
            self.awaiting_property = "width"
            self._prompt(
                canvas,
                "Especifique ancho de la puerta:",
            )
            return True

        if upper in (
            "H",
            "ALTURA",
            "HEIGHT",
        ):
            self.awaiting_property = "height"
            self._prompt(
                canvas,
                "Especifique altura de la puerta:",
            )
            return True

        if upper in (
            "I",
            "IZQ",
            "LEFT",
        ):
            self.handedness = Door.LEFT
            self._status(
                canvas,
                "DOOR: mano izquierda",
            )
            return True

        if upper in (
            "D",
            "DER",
            "RIGHT",
        ):
            self.handedness = Door.RIGHT
            self._status(
                canvas,
                "DOOR: mano derecha",
            )
            return True

        if upper in (
            "IN",
            "INT",
            "INTERIOR",
            "INWARD",
        ):
            self.swing_direction = Door.INWARD
            self._status(
                canvas,
                "DOOR: apertura interior",
            )
            return True

        if upper in (
            "OUT",
            "EXT",
            "EXTERIOR",
            "OUTWARD",
        ):
            self.swing_direction = Door.OUTWARD
            self._status(
                canvas,
                "DOOR: apertura exterior",
            )
            return True

        if upper in (
            "VOLTEAR",
            "FLIP",
        ):
            self.handedness = (
                Door.RIGHT
                if self.handedness == Door.LEFT
                else Door.LEFT
            )
            self._status(
                canvas,
                "DOOR: sentido invertido",
            )
            return True

        return False

    def key_press(
        self,
        event,
        canvas,
    ):
        if event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        self.selected_wall = None
        self.awaiting_property = None

        if canvas is not None:
            canvas.highlight.clear()
            self._prompt(
                canvas,
                "Comando:",
            )
            self._status(
                canvas,
                "DOOR cancelado",
            )
            canvas.update()

        print("DOOR cancelado")

    def deactivate(self):
        self.selected_wall = None
        self.awaiting_property = None
        print("DOOR desactivado")
