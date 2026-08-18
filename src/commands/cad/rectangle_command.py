"""
AI Architecture Studio
CAD Command - Rectangle Profesional

Dynamic Input Universal - Package 3.2
"""

import math
import re

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class RectangleCommand(BaseCommand):

    POLAR_WIDTH_PATTERN = re.compile(
        r"^@?([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))"
        r"<([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))$"
    )

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "RECTANGLE"
        self.first_corner = None

        # Compatibilidad con Canvas Dynamic Input.
        self.first_point = None

        self.current_point = None
        self.current_width = 0.0
        self.current_height = 0.0

        self._previous_distance_label = None
        self._previous_angle_label = None

    # ---------------------------------------------------------
    # SERVICIOS
    # ---------------------------------------------------------

    def get_dynamic_input_manager(self, canvas):
        scene = getattr(canvas, "scene", None)
        kernel = getattr(scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get(
            "dynamic_input_manager"
        )

    def get_main_window(self, canvas):
        window_getter = getattr(
            canvas,
            "window",
            None,
        )

        if not callable(window_getter):
            return None

        return window_getter()

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

    def show_status(self, canvas, text):
        main_window = self.get_main_window(canvas)

        if (
            main_window is not None
            and hasattr(main_window, "statusBar")
        ):
            main_window.statusBar().showMessage(text)

    def get_canvas_point(self, canvas):
        getter = getattr(
            canvas,
            "get_input_point",
            None,
        )

        if callable(getter):
            return getter()

        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    # ---------------------------------------------------------
    # DYNAMIC INPUT
    # ---------------------------------------------------------

    def _configure_dynamic_input(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is None:
            return

        if self._previous_distance_label is None:
            self._previous_distance_label = (
                manager.distance_field.label
            )
            self._previous_angle_label = (
                manager.angle_field.label
            )

        manager.distance_field.label = "Ancho"
        manager.angle_field.label = "Alto"

        manager.set_base_point(
            self.first_corner
        )
        manager.reset_fields()
        manager.set_prompt("Ancho / Alto")
        manager.show()

    def _restore_dynamic_input(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is None:
            return

        manager.distance_field.label = (
            self._previous_distance_label
            or "Distancia"
        )
        manager.angle_field.label = (
            self._previous_angle_label
            or "Ángulo"
        )

        manager.reset()

        self._previous_distance_label = None
        self._previous_angle_label = None

    def dynamic_input_value(self, manager):
        """
        Formato interno:
            RECT|ancho|alto|ángulo

        Rectángulo ortogonal:
            Ancho = 10
            Alto  = 5

        Rectángulo orientado:
            Ancho = @10<30
            Alto  = 5
        """

        width_text = (
            manager.distance_field.value.strip()
        )
        height_text = (
            manager.angle_field.value.strip()
        )

        if not width_text:
            width_text = f"{abs(self.current_width):.12g}"

        if not height_text:
            height_text = f"{abs(self.current_height):.12g}"

        if not width_text or not height_text:
            return None

        angle = 0.0

        polar_match = self.POLAR_WIDTH_PATTERN.match(
            width_text
        )

        if polar_match:
            width_text = polar_match.group(1)
            angle = self._to_float(
                polar_match.group(2)
            )
        else:
            # El cuadrante del cursor define los signos en modo
            # ortogonal, igual que al seleccionar dos esquinas.
            width = self._to_float(width_text)
            height = self._to_float(height_text)

            if self.current_width < 0:
                width = -abs(width)
            else:
                width = abs(width)

            if self.current_height < 0:
                height = -abs(height)
            else:
                height = abs(height)

            return (
                f"RECT|{width:.12g}|"
                f"{height:.12g}|0"
            )

        width = abs(self._to_float(width_text))
        height = self._to_float(height_text)

        # Altura positiva queda a la izquierda del eje orientado;
        # el signo puede invertirse escribiendo una altura negativa.
        return (
            f"RECT|{width:.12g}|"
            f"{height:.12g}|{angle:.12g}"
        )

    # ---------------------------------------------------------
    # GEOMETRÍA
    # ---------------------------------------------------------

    @staticmethod
    def _to_float(value):
        return float(
            str(value).strip().replace(",", ".")
        )

    def _dimensions_from_cursor(self, point):
        dx = point.x - self.first_corner.x
        dy = point.y - self.first_corner.y

        self.current_width = dx
        self.current_height = dy
        self.current_point = point

        return dx, dy

    def _preview_from_manager(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        width = self.current_width
        height = self.current_height
        angle = 0.0

        if manager is not None:
            width_value = (
                manager.distance_field.numeric_value()
            )
            height_value = (
                manager.angle_field.numeric_value()
            )

            raw_width = (
                manager.distance_field.value.strip()
            )

            polar_match = self.POLAR_WIDTH_PATTERN.match(
                raw_width
            )

            if polar_match:
                width = abs(
                    self._to_float(
                        polar_match.group(1)
                    )
                )
                angle = self._to_float(
                    polar_match.group(2)
                )

                if height_value is not None:
                    height = height_value
            else:
                if width_value is not None:
                    width = (
                        -abs(width_value)
                        if self.current_width < 0
                        else abs(width_value)
                    )

                if height_value is not None:
                    height = (
                        -abs(height_value)
                        if self.current_height < 0
                        else abs(height_value)
                    )

        return GeometryBuilder.create_oriented_rectangle(
            self.first_corner,
            width,
            height,
            angle,
        )

    def _create_rectangle(
        self,
        canvas,
        width,
        height,
        angle,
    ):
        if (
            abs(width) <= 1e-9
            or abs(height) <= 1e-9
        ):
            message = (
                "RECTANGLE: ancho y alto deben "
                "ser mayores que cero"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        rectangle = (
            GeometryBuilder.create_oriented_rectangle(
                self.first_corner,
                width,
                height,
                angle,
            )
        )

        canvas.scene.add_element(rectangle)

        if self.app_core:
            self.app_core.history.push(
                AddAction(
                    canvas.scene,
                    rectangle,
                )
            )

        print(
            "RECTANGLE creado: "
            f"ancho={abs(width):.6g}, "
            f"alto={abs(height):.6g}, "
            f"ángulo={angle % 360.0:.6g}°"
        )

        self._finish(canvas)
        return True

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if self.first_corner is None:
            return

        point = self.get_canvas_point(canvas)
        self._dimensions_from_cursor(point)

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(
                self.first_corner
            )
            manager.update_point(point)

        canvas.preview_geometry = (
            self._preview_from_manager(canvas)
        )
        canvas.update()

    def mouse_press(self, event, canvas):
        point = self.get_canvas_point(canvas)

        if self.first_corner is None:
            self.first_corner = point
            self.first_point = point
            self.current_point = point

            print(
                f"RECTANGLE: Primera esquina {point}"
            )

            self._configure_dynamic_input(canvas)

            self.set_prompt(
                canvas,
                "Especifique ancho y alto:",
            )
            self.show_status(
                canvas,
                "RECTANGLE: indique esquina opuesta "
                "o escriba Ancho y Alto",
            )

            canvas.update()
            return

        width, height = self._dimensions_from_cursor(
            point
        )

        self._create_rectangle(
            canvas,
            width,
            height,
            0.0,
        )

    # ---------------------------------------------------------
    # TEXTO
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if not value.startswith("RECT|"):
            self.show_status(
                canvas,
                "RECTANGLE: entrada dinámica inválida",
            )
            return False

        parts = value.split("|")

        if len(parts) != 4:
            return False

        try:
            width = self._to_float(parts[1])
            height = self._to_float(parts[2])
            angle = self._to_float(parts[3])
        except ValueError:
            self.show_status(
                canvas,
                "RECTANGLE: valores numéricos inválidos",
            )
            return False

        return self._create_rectangle(
            canvas,
            width,
            height,
            angle,
        )

    # ---------------------------------------------------------
    # FINALIZACIÓN
    # ---------------------------------------------------------

    def _finish(self, canvas):
        self._restore_dynamic_input(canvas)

        self.first_corner = None
        self.first_point = None
        self.current_point = None
        self.current_width = 0.0
        self.current_height = 0.0

        canvas.preview_geometry = None
        canvas.update()

        self.set_prompt(canvas, "Comando:")
        self.show_status(
            canvas,
            "RECTANGLE creado",
        )

        tool_manager = getattr(
            canvas,
            "tool_manager",
            None,
        )

        if tool_manager is not None:
            tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        if (
            self.first_corner is None
            and self.first_point is None
        ):
            return

        if canvas is not None:
            self._restore_dynamic_input(canvas)

            canvas.preview_geometry = None
            canvas.update()

            self.set_prompt(canvas, "Comando:")
            self.show_status(
                canvas,
                "RECTANGLE cancelado",
            )

        self.first_corner = None
        self.first_point = None
        self.current_point = None
        self.current_width = 0.0
        self.current_height = 0.0

        print("RECTANGLE finalizado")

    def deactivate(self):
        self.first_corner = None
        self.first_point = None
        self.current_point = None
        self.current_width = 0.0
        self.current_height = 0.0

        print("Comando RECTANGLE desactivado")
