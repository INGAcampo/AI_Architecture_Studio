"""Comando OPENING — Architectural Core 5.0.5.1."""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_wall_opening_action import AddWallOpeningAction
from engines.architectural.opening_engine import OpeningEngine
from engines.geometry.point import Point


class OpeningCommand(BaseCommand):
    PICK_TOLERANCE = 0.75

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "OPENING"
        self.width = OpeningEngine.DEFAULT_WIDTH
        self.height = OpeningEngine.DEFAULT_HEIGHT
        self.sill_height = OpeningEngine.DEFAULT_SILL_HEIGHT
        self.selected_wall = None
        self.awaiting_property = None

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
            command_line.focus_input()

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
        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def _walls(self, scene):
        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        return [
            item for item in elements
            if item.__class__.__name__ == "Wall"
            and getattr(item, "visible", True)
        ]

    def begin(self, canvas):
        self.selected_wall = None
        self._prompt(
            canvas,
            f"Seleccione muro [A={self.width:g}, "
            f"H={self.height:g}, P={self.sill_height:g}]:",
        )
        self._status(
            canvas,
            "OPENING activo: seleccione el muro anfitrión",
        )

    def mouse_press(self, event, canvas):
        scene = self._scene(canvas)
        point = self._point(canvas)

        if scene is None:
            self._status(canvas, "OPENING: no hay una escena activa")
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
                    "OPENING: no se encontró un muro cercano",
                )
                return

            self.selected_wall = result["wall"]
            canvas.highlight.set(self.selected_wall)
            self._prompt(canvas, "Indique el centro del hueco sobre el muro:")
            self._status(
                canvas,
                "OPENING: muro seleccionado; indique la posición",
            )
            canvas.update()
            return

        opening = OpeningEngine.create_opening(
            self.selected_wall,
            point,
            width=self.width,
            height=self.height,
            sill_height=self.sill_height,
        )
        OpeningEngine.add_to_wall(self.selected_wall, opening)

        if self.app_core is not None:
            self.app_core.history.push(
                AddWallOpeningAction(
                    scene,
                    self.selected_wall,
                    opening,
                )
            )

        scene.wall_network_signature = None
        print(
            "OPENING creado: "
            f"ancho={opening.width:g} m, "
            f"altura={opening.height:g} m, "
            f"antepecho={opening.sill_height:g} m"
        )

        self.selected_wall = None
        canvas.highlight.clear()
        self._prompt(
            canvas,
            f"Seleccione muro [A={self.width:g}, "
            f"H={self.height:g}, P={self.sill_height:g}]:",
        )
        self._status(
            canvas,
            "OPENING creado. Seleccione otro muro o pulse ESC",
        )
        canvas.update()

    def _set_numeric_property(self, value, canvas):
        try:
            number = float(str(value).replace(",", "."))
        except ValueError:
            self._status(canvas, "OPENING: valor numérico no válido")
            return True

        if self.awaiting_property == "width":
            if number <= 0.0:
                self._status(canvas, "OPENING: el ancho debe ser mayor que cero")
                return True
            self.width = number
            label = "ancho"
        elif self.awaiting_property == "height":
            if number <= 0.0:
                self._status(canvas, "OPENING: la altura debe ser mayor que cero")
                return True
            self.height = number
            label = "altura"
        else:
            if number < 0.0:
                self._status(canvas, "OPENING: el antepecho no puede ser negativo")
                return True
            self.sill_height = number
            label = "antepecho"

        self.awaiting_property = None
        self._status(canvas, f"OPENING: {label}={number:g} m")
        self._prompt(
            canvas,
            "Indique el centro del hueco:"
            if self.selected_wall is not None
            else "Seleccione muro:",
        )
        return True

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()
        if not value:
            return False

        if self.awaiting_property is not None:
            return self._set_numeric_property(value, canvas)

        upper = value.upper()
        if upper in ("A", "ANCHO", "WIDTH"):
            self.awaiting_property = "width"
            self._prompt(canvas, "Especifique ancho del hueco:")
            return True
        if upper in ("H", "ALTURA", "HEIGHT"):
            self.awaiting_property = "height"
            self._prompt(canvas, "Especifique altura del hueco:")
            return True
        if upper in ("P", "ANTEPECHO", "SILL"):
            self.awaiting_property = "sill"
            self._prompt(canvas, "Especifique altura de antepecho:")
            return True
        return False

    def key_press(self, event, canvas):
        if event.key() == Qt.Key_Escape:
            self.cancel(canvas)

    def cancel(self, canvas=None):
        self.selected_wall = None
        self.awaiting_property = None
        if canvas is not None:
            canvas.highlight.clear()
            self._prompt(canvas, "Comando:")
            self._status(canvas, "OPENING cancelado")
            canvas.update()
        print("OPENING cancelado")

    def deactivate(self):
        self.selected_wall = None
        self.awaiting_property = None
