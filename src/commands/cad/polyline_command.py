"""
AI Architecture Studio
CAD Command - Polyline Profesional

Dynamic Input Universal - Package 3.1.1
"""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class PolylineCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "PLINE"
        self.points = []

        # Canvas utiliza first_point para detectar que Dynamic Input
        # puede trabajar. En PLINE representa el último vértice.
        self.first_point = None

    # ---------------------------------------------------------
    # SERVICIOS Y UI
    # ---------------------------------------------------------

    def get_dynamic_input_manager(self, canvas):
        scene = getattr(canvas, "scene", None)
        kernel = getattr(scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get(
            "dynamic_input_manager"
        )

    def get_ortho_manager(self, canvas):
        scene = getattr(canvas, "scene", None)
        kernel = getattr(scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get(
            "ortho_manager"
        )

    def get_main_window(self, canvas):
        window = getattr(canvas, "window", None)

        if not callable(window):
            return None

        return window()

    def set_prompt(self, canvas, text):
        main_window = self.get_main_window(canvas)

        if main_window is None:
            return

        command_line = getattr(
            main_window,
            "command_line",
            None,
        )

        if command_line is not None:
            command_line.set_prompt(text)

    def focus_command_line(self, canvas):
        main_window = self.get_main_window(canvas)

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
        main_window = self.get_main_window(canvas)

        if (
            main_window is not None
            and hasattr(main_window, "statusBar")
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

        return Point(x, y, 0.0)

    def apply_ortho(self, canvas, point):
        if self.first_point is None:
            return point

        ortho_manager = self.get_ortho_manager(
            canvas
        )

        if (
            ortho_manager is None
            or not getattr(
                ortho_manager,
                "enabled",
                False,
            )
        ):
            return point

        return ortho_manager.apply(
            self.first_point,
            point,
        )

    def _prepare_next_segment(self, canvas):
        if not self.points:
            self.first_point = None
            return

        self.first_point = self.points[-1]

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(
                self.first_point
            )
            manager.reset_fields()
            manager.set_prompt(
                "Distancia / Ángulo"
            )
            manager.show()

        self.set_prompt(
            canvas,
            "Especifique siguiente punto "
            "[Enter/Esc para finalizar]:",
        )

        self.show_status(
            canvas,
            "PLINE: especifique el siguiente punto",
        )

        canvas.setFocus()

    def _append_point(self, point, canvas):
        if self.points:
            previous = self.points[-1]

            if point.distance_to(previous) <= 1e-9:
                message = (
                    "PLINE: el nuevo punto debe ser "
                    "distinto del anterior"
                )
                print(message)
                self.show_status(canvas, message)
                return False

        self.points.append(point)

        print(
            f"PLINE: Punto {len(self.points)} {point}"
        )

        if len(self.points) == 1:
            self.set_prompt(
                canvas,
                "Especifique siguiente punto:",
            )
        else:
            self.set_prompt(
                canvas,
                "Especifique siguiente punto "
                "[Enter/Esc para finalizar]:",
            )

        self._prepare_next_segment(canvas)

        canvas.preview_geometry = None
        canvas.update()
        return True

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if not self.points:
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
            current_point = manager.constrained_point(
                self.first_point
            )

        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.first_point,
                current_point,
            )
        )

        canvas.update()

    def mouse_press(self, event, canvas):
        point = self.get_canvas_point(canvas)

        if self.first_point is not None:
            point = self.apply_ortho(
                canvas,
                point,
            )

        self._append_point(point, canvas)

    # ---------------------------------------------------------
    # ENTRADA DE TEXTO
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        value = str(text).strip()

        if not value:
            return False

        direction_point = self.get_canvas_point(
            canvas
        )

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
            self.show_status(canvas, message)
            self.focus_command_line(canvas)
            return False

        accepted = self._append_point(
            point,
            canvas,
        )

        if accepted:
            canvas.setFocus()

        return accepted

    # ---------------------------------------------------------
    # FINALIZACIÓN
    # ---------------------------------------------------------

    def _create_polyline(self, canvas):
        if len(self.points) < 2:
            return False

        polyline = GeometryBuilder.create_polyline(
            list(self.points),
            closed=False,
        )

        canvas.scene.add_element(polyline)

        if self.app_core:
            self.app_core.history.push(
                AddAction(
                    canvas.scene,
                    polyline,
                )
            )

        print(
            "PLINE creada con "
            f"{len(self.points)} puntos"
        )

        return True

    def finish(self, canvas=None):
        created = False

        if canvas is not None:
            created = self._create_polyline(
                canvas
            )

            manager = self.get_dynamic_input_manager(
                canvas
            )

            if manager is not None:
                manager.reset()

            canvas.preview_geometry = None
            canvas.current_snap_point = None
            canvas.current_snap_type = None
            canvas.update()

            if created:
                self.show_status(
                    canvas,
                    "PLINE creada",
                )
            else:
                self.show_status(
                    canvas,
                    "PLINE cancelada: se requieren "
                    "al menos dos puntos",
                )

            self.set_prompt(canvas, "Comando:")

        self.points = []
        self.first_point = None

        return created

    def key_press(self, event, canvas):
        if event.key() not in (
            Qt.Key_Return,
            Qt.Key_Enter,
        ):
            return

        # ENTER sin datos en el panel finaliza la polilínea.
        self.finish(canvas)

        tool_manager = getattr(
            canvas,
            "tool_manager",
            None,
        )

        if tool_manager is not None:
            tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        # Evita una segunda finalización cuando ToolManager
        # vuelve a cancelar después de que la PLINE ya fue creada.
        if not self.points and self.first_point is None:
            return

        # En PLINE, ESC finaliza la geometría si ya hay
        # por lo menos dos vértices.
        created = self.finish(canvas)

        if created:
            print("PLINE finalizada")
        else:
            print("PLINE cancelada")

    def deactivate(self):
        self.points = []
        self.first_point = None

        print("Comando PLINE desactivado")
