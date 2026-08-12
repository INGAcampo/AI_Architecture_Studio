"""
AI Architecture Studio
CAD Command - Offset Profesional

Dynamic Input Universal - Package 3.8
"""

from commands.base_command import BaseCommand
from core.history.offset_action import OffsetAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class OffsetCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "OFFSET"

        self.elements = []
        self.distance = None
        self.side_point = None

        # Mantiene activo Dynamic Input en el Canvas.
        self.first_point = None
        self.current_point = None

    # ---------------------------------------------------------
    # ACTIVACIÓN Y SERVICIOS
    # ---------------------------------------------------------

    def activate(self):
        super().activate()

        print(
            "OFFSET activo: selecciona uno o varios objetos, "
            "escribe la distancia y señala el lado"
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
            if GeometryBuilder.can_offset_element(
                element
            )
        ]

        if not self.elements:
            print("OFFSET: No hay objetos compatibles seleccionados")
            self.show_status(
                canvas,
                "OFFSET: selecciona al menos un objeto "
                "compatible antes de activar el comando",
            )
            return False

        print(
            f"OFFSET: {len(self.elements)} objeto(s) "
            "seleccionado(s)"
        )

        return True

    def configure_dynamic_input(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is None:
            return

        if self.first_point is None:
            self.first_point = self.get_canvas_point(
                canvas
            )

        manager.set_base_point(
            self.first_point
        )
        manager.reset_fields()
        manager.set_prompt(
            "Distancia OFFSET"
        )
        manager.show()

    # ---------------------------------------------------------
    # PREVISUALIZACIÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if not self.capture_selection(canvas):
            return

        point = self.get_canvas_point(canvas)
        self.current_point = point

        if self.first_point is None:
            self.first_point = point
            self.configure_dynamic_input(canvas)

        if self.distance is None:
            canvas.preview_geometry = None
            canvas.update()
            return

        # Guía visual del lado elegido. El objeto definitivo
        # se crea únicamente al confirmar con clic.
        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.first_point,
                point,
            )
        )

        canvas.update()

    # ---------------------------------------------------------
    # ENTRADA NUMÉRICA
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        if not self.capture_selection(canvas):
            return False

        value = str(text or "").strip().replace(
            ",",
            ".",
        )

        try:
            distance = float(value)

        except (TypeError, ValueError):
            message = (
                f"OFFSET: distancia no válida: {text}"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        if distance <= 0.0:
            message = (
                "OFFSET: la distancia debe ser mayor que cero"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        self.distance = distance

        if self.first_point is None:
            self.first_point = self.get_canvas_point(
                canvas
            )

        print(
            f"OFFSET: Distancia {self.distance:g}"
        )

        self.set_prompt(
            canvas,
            "Señale el lado del desplazamiento:",
        )
        self.show_status(
            canvas,
            "OFFSET: haz clic en el lado deseado",
        )

        canvas.update()
        return True

    # ---------------------------------------------------------
    # RATÓN Y EJECUCIÓN
    # ---------------------------------------------------------

    def mouse_press(self, event, canvas):
        if not self.capture_selection(canvas):
            canvas.tool_manager.cancel(canvas)
            return

        if self.distance is None:
            self.first_point = self.get_canvas_point(
                canvas
            )
            self.configure_dynamic_input(canvas)

            self.set_prompt(
                canvas,
                "Especifique distancia OFFSET:",
            )
            self.show_status(
                canvas,
                "OFFSET: escribe una distancia mayor que cero",
            )
            return

        self.side_point = self.get_canvas_point(
            canvas
        )

        self.complete_offset(canvas)

    def complete_offset(self, canvas):
        scene = getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

        if scene is None:
            print("OFFSET: escena no disponible")
            return False

        created_elements = []

        for element in self.elements:
            offset_element = (
                GeometryBuilder.create_offset_element(
                    element,
                    self.distance,
                    self.side_point,
                )
            )

            if offset_element is None:
                continue

            scene.add_element(offset_element)
            created_elements.append(offset_element)

        if (
            created_elements
            and self.app_core is not None
        ):
            self.app_core.history.push(
                OffsetAction(
                    scene,
                    created_elements,
                )
            )

        print(
            f"OFFSET completado: "
            f"{len(created_elements)} objeto(s) creado(s), "
            f"distancia={self.distance:g}"
        )

        self.finish(canvas)
        return bool(created_elements)

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
        self.distance = None
        self.side_point = None
        self.first_point = None
        self.current_point = None

        self.set_prompt(canvas, "Comando:")
        self.show_status(
            canvas,
            "OFFSET completado",
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
            and self.distance is None
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
                "OFFSET cancelado",
            )

        self.elements = []
        self.distance = None
        self.side_point = None
        self.first_point = None
        self.current_point = None

        print("OFFSET finalizado")

    def deactivate(self):
        self.elements = []
        self.distance = None
        self.side_point = None
        self.first_point = None
        self.current_point = None

        print("OFFSET desactivado")
