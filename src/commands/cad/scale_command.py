"""
AI Architecture Studio
CAD Command - Scale Profesional

Dynamic Input Universal - Package 3.6
"""

from commands.base_command import BaseCommand
from core.history.scale_action import ScaleAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class ScaleCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "SCALE"
        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_point = None

    # ---------------------------------------------------------
    # ACTIVACIÓN Y SERVICIOS
    # ---------------------------------------------------------

    def activate(self):
        super().activate()

        print(
            "SCALE activo: selecciona uno o varios objetos, "
            "indica el punto base y escribe el factor"
        )

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

    def capture_selection(self, canvas):
        if self.elements:
            return True

        selected = (
            canvas.selection_manager
            .selected_elements()
        )

        self.elements = [
            element
            for element in selected
            if TransformManager.can_scale_element(
                element
            )
        ]

        if not self.elements:
            print("SCALE: No hay objetos compatibles seleccionados")
            self.show_status(
                canvas,
                "SCALE: selecciona al menos un objeto "
                "compatible antes de activar el comando",
            )
            return False

        print(
            f"SCALE: {len(self.elements)} objeto(s) "
            "seleccionado(s)"
        )

        return True

    # ---------------------------------------------------------
    # DYNAMIC INPUT Y PREVISUALIZACIÓN
    # ---------------------------------------------------------

    def configure_dynamic_input(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is None:
            return

        manager.set_base_point(
            self.base_point
        )
        manager.reset_fields()
        manager.set_prompt(
            "Factor de escala"
        )
        manager.show()

    def mouse_move(self, event, canvas):
        if self.base_point is None:
            return

        self.current_point = self.get_canvas_point(
            canvas
        )

        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.base_point,
                self.current_point,
            )
        )

        canvas.update()

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_press(self, event, canvas):
        if not self.capture_selection(canvas):
            canvas.tool_manager.cancel(canvas)
            return

        if self.base_point is not None:
            return

        self.base_point = self.get_canvas_point(
            canvas
        )
        self.first_point = self.base_point
        self.current_point = self.base_point

        print(
            f"SCALE: Punto base {self.base_point}"
        )

        self.configure_dynamic_input(canvas)

        self.set_prompt(
            canvas,
            "Especifique factor de escala:",
        )
        self.show_status(
            canvas,
            "SCALE: escribe un factor mayor que cero",
        )

        canvas.update()

    # ---------------------------------------------------------
    # ENTRADA NUMÉRICA
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        if self.base_point is None:
            return False

        value = str(text or "").strip().replace(
            ",",
            ".",
        )

        try:
            scale_factor = float(value)

        except (TypeError, ValueError):
            message = (
                f"SCALE: factor no válido: {text}"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        if scale_factor <= 0.0:
            message = (
                "SCALE: el factor debe ser mayor que cero"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        return self.complete_scale(
            canvas,
            scale_factor,
        )

    # ---------------------------------------------------------
    # EJECUCIÓN E HISTORIAL
    # ---------------------------------------------------------

    def complete_scale(
        self,
        canvas,
        scale_factor,
    ):
        scaled_elements = (
            TransformManager.scale_elements(
                self.elements,
                scale_factor,
                self.base_point.x,
                self.base_point.y,
                self.base_point.z,
            )
        )

        if (
            scaled_elements
            and self.app_core is not None
        ):
            self.app_core.history.push(
                ScaleAction(
                    scaled_elements,
                    scale_factor,
                    self.base_point.x,
                    self.base_point.y,
                    self.base_point.z,
                )
            )

        print(
            f"SCALE completado: "
            f"{len(scaled_elements)} objeto(s), "
            f"factor={scale_factor:g}"
        )

        self.finish(canvas)
        return bool(scaled_elements)

    # ---------------------------------------------------------
    # FINALIZACIÓN
    # ---------------------------------------------------------

    def finish(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.reset()

        canvas.preview_geometry = None
        canvas.current_snap_point = None
        canvas.current_snap_type = None

        canvas.selection_manager.clear()
        canvas.highlight.clear()
        canvas.element_selected.emit(None)

        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_point = None

        self.set_prompt(canvas, "Comando:")
        self.show_status(
            canvas,
            "SCALE completado",
        )

        canvas.update()

        tool_manager = getattr(
            canvas,
            "tool_manager",
            None,
        )

        if tool_manager is not None:
            tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        if (
            not self.elements
            and self.base_point is None
            and self.first_point is None
        ):
            return

        if canvas is not None:
            manager = self.get_dynamic_input_manager(
                canvas
            )

            if manager is not None:
                manager.reset()

            canvas.preview_geometry = None
            canvas.update()

            self.set_prompt(canvas, "Comando:")
            self.show_status(
                canvas,
                "SCALE cancelado",
            )

        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_point = None

        print("SCALE finalizado")

    def deactivate(self):
        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_point = None

        print("Comando SCALE desactivado")
