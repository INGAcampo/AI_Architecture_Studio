


"""
AI Architecture Studio
CAD Command - Line Profesional

Dynamic Input v1
"""

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point
from models.cad_line import CadLine


class LineCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "LINE"
        self.first_point = None

    # ---------------------------------------------------------
    # SERVICIOS Y UI
    # ---------------------------------------------------------

    def get_dynamic_input_manager(
        self,
        canvas,
    ):
        scene = getattr(
            canvas,
            "scene",
            None,
        )
        kernel = getattr(
            scene,
            "kernel",
            None,
        )

        if kernel is None:
            return None

        return kernel.services.get(
            "dynamic_input_manager"
        )

    def get_ortho_manager(self, canvas):
        scene = getattr(
            canvas,
            "scene",
            None,
        )

        kernel = getattr(
            scene,
            "kernel",
            None,
        )

        if kernel is None:
            return None

        return kernel.services.get(
            "ortho_manager"
        )

    def get_main_window(self, canvas):
        window = getattr(
            canvas,
            "window",
            None,
        )

        if not callable(window):
            return None

        return window()

    def set_prompt(self, canvas, text):
        main_window = self.get_main_window(
            canvas
        )

        if main_window is None:
            return

        command_line = getattr(
            main_window,
            "command_line",
            None,
        )

        if command_line is None:
            return

        command_line.set_prompt(text)

    def focus_command_line(self, canvas):
        main_window = self.get_main_window(
            canvas
        )

        if main_window is None:
            return

        command_line = getattr(
            main_window,
            "command_line",
            None,
        )

        if command_line is not None:
            command_line.focus_input()

    def show_status(self, canvas, message):
        main_window = self.get_main_window(
            canvas
        )

        if (
            main_window is not None
            and hasattr(
                main_window,
                "statusBar",
            )
        ):
            main_window.statusBar().showMessage(
                message
            )

    # ---------------------------------------------------------
    # PUNTOS
    # ---------------------------------------------------------

    def get_canvas_point(self, canvas):
        get_input_point = getattr(
            canvas,
            "get_input_point",
            None,
        )

        if callable(get_input_point):
            return get_input_point()

        x, y = canvas.cursor_position

        return Point(
            x,
            y,
            0.0,
        )

    def apply_ortho(
        self,
        canvas,
        point,
    ):
        if self.first_point is None:
            return point

        ortho_manager = (
            self.get_ortho_manager(
                canvas
            )
        )

        if ortho_manager is None:
            return point

        return ortho_manager.apply(
            self.first_point,
            point,
        )

    def _set_first_point(
        self,
        point,
        canvas,
    ):
        self.first_point = point

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(point)
            manager.reset_fields()
            manager.set_prompt(
                "Distancia / Ángulo"
            )
            manager.show()

        print(
            f"LINE: Primer punto {point}"
        )

        self.set_prompt(
            canvas,
            "Especifique siguiente punto:",
        )

        self.show_status(
            canvas,
            "LINE: especifique el siguiente punto",
        )

        canvas.setFocus()

    def _create_line(
        self,
        point,
        canvas,
    ):
        if (
            point.distance_to(
                self.first_point
            )
            <= 1e-9
        ):
            message = (
                "LINE: el segundo punto debe "
                "ser distinto del primero"
            )

            print(message)
            self.show_status(
                canvas,
                message,
            )
            return False

        line = (
            GeometryBuilder.create_line(
                self.first_point,
                point,
            )
        )

        cad_line = CadLine(line)

        canvas.scene.add_element(
            cad_line
        )

        if self.app_core:
            self.app_core.history.push(
                AddAction(
                    canvas.scene,
                    cad_line,
                )
            )

        print(
            f"LINE creada: {line}"
        )

        self.first_point = None

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.reset()

        canvas.preview_geometry = None
        canvas.current_snap_point = None
        canvas.current_snap_type = None
        canvas.update()

        self.set_prompt(
            canvas,
            "Especifique primer punto:",
        )

        self.show_status(
            canvas,
            "LINE creada. Especifique el primer punto de la siguiente línea",
        )

        canvas.setFocus()

        return True

    def accept_point(
        self,
        point,
        canvas,
    ):
        if self.first_point is None:
            self._set_first_point(
                point,
                canvas,
            )
            return True

        return self._create_line(
            point,
            canvas,
        )

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(
        self,
        event,
        canvas,
    ):
        if self.first_point is None:
            canvas.preview_geometry = None
            canvas.update()
            return

        current_point = self.get_canvas_point(
            canvas
        )

        current_point = self.apply_ortho(
            canvas,
            current_point,
        )

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(
                self.first_point
            )
            manager.update_point(
                current_point
            )
            current_point = (
                manager.constrained_point(
                    self.first_point
                )
            )

        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.first_point,
                current_point,
            )
        )

        canvas.update()

    def mouse_press(
        self,
        event,
        canvas,
    ):
        point = self.get_canvas_point(
            canvas
        )

        if self.first_point is not None:
            point = self.apply_ortho(
                canvas,
                point,
            )

        self.accept_point(
            point,
            canvas,
        )

    # ---------------------------------------------------------
    # ENTRADA DE TEXTO
    # ---------------------------------------------------------

    def handle_text_input(
        self,
        text,
        canvas,
    ):
        value = str(text).strip()

        if not value:
            return False

        direction_point = (
            self.get_canvas_point(
                canvas
            )
        )

        # Para una distancia directa, ORTHO determina
        # la dirección mediante la posición actual del cursor.
        if (
            self.first_point is not None
            and CoordinateParser.DISTANCE_PATTERN.match(
                value
            )
        ):
            direction_point = self.apply_ortho(
                canvas,
                direction_point,
            )

        try:
            point = CoordinateParser.parse(
                value,
                base_point=self.first_point,
                direction_point=direction_point,
            )

        except CoordinateParseError as error:
            message = f"Entrada no válida: {error}"

            print(message)

            self.show_status(
                canvas,
                message,
            )

            self.focus_command_line(canvas)
            return False

        accepted = self.accept_point(
            point,
            canvas,
        )

        if accepted:
            canvas.setFocus()

        return accepted

    # ---------------------------------------------------------
    # CANCELACIÓN
    # ---------------------------------------------------------

    def cancel(self, canvas=None):
        self.first_point = None

        if canvas:
            manager = self.get_dynamic_input_manager(
                canvas
            )

            if manager is not None:
                manager.reset()

            canvas.preview_geometry = None
            canvas.current_snap_point = None
            canvas.current_snap_type = None
            canvas.update()

            self.set_prompt(
                canvas,
                "Comando:",
            )

        print("LINE cancelada")

    def deactivate(self):
        self.first_point = None

        print(
            "Comando LINE desactivado"
        )