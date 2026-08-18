"""
AI Architecture Studio
CAD Command - Mirror Profesional

Dynamic Input Universal - Package 3.7
"""

from commands.base_command import BaseCommand
from core.history.mirror_action import MirrorAction
from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class MirrorCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "MIRROR"

        self.elements = []
        self.axis_start = None
        self.axis_end = None

        # Canvas usa first_point para Dynamic Input.
        self.first_point = None
        self.current_point = None

    # ---------------------------------------------------------
    # ACTIVACIÓN Y SERVICIOS
    # ---------------------------------------------------------

    def activate(self):
        super().activate()

        print(
            "MIRROR activo: selecciona uno o varios objetos "
            "y define el eje mediante dos puntos"
        )

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
            if TransformManager.can_mirror_element(
                element
            )
        ]

        if not self.elements:
            print("MIRROR: No hay objetos compatibles seleccionados")
            self.show_status(
                canvas,
                "MIRROR: selecciona al menos un objeto "
                "compatible antes de activar el comando",
            )
            return False

        print(
            f"MIRROR: {len(self.elements)} objeto(s) "
            "seleccionado(s)"
        )

        return True

    # ---------------------------------------------------------
    # RESTRICCIONES Y DYNAMIC INPUT
    # ---------------------------------------------------------

    def apply_ortho(self, canvas, point):
        if self.axis_start is None:
            return point

        ortho = self.get_ortho_manager(canvas)

        if (
            ortho is None
            or not getattr(ortho, "enabled", False)
        ):
            return point

        return ortho.apply(
            self.axis_start,
            point,
        )

    def configure_dynamic_input(self, canvas):
        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is None:
            return

        manager.set_base_point(
            self.axis_start
        )
        manager.reset_fields()
        manager.set_prompt(
            "Longitud / Ángulo del eje"
        )
        manager.show()

    def update_preview(self, canvas, point):
        point = self.apply_ortho(
            canvas,
            point,
        )

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(
                self.axis_start
            )
            manager.update_point(point)

            point = manager.constrained_point(
                self.axis_start
            )

        self.current_point = point

        # Vista previa compatible con el renderer actual:
        # línea temporal que representa el eje de simetría.
        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.axis_start,
                point,
            )
        )

        canvas.update()

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if self.axis_start is None:
            return

        self.update_preview(
            canvas,
            self.get_canvas_point(canvas),
        )

    def mouse_press(self, event, canvas):
        if not self.capture_selection(canvas):
            canvas.tool_manager.cancel(canvas)
            return

        point = self.get_canvas_point(canvas)

        if self.axis_start is None:
            self.axis_start = point
            self.first_point = point
            self.current_point = point

            print(
                f"MIRROR: Primer punto {point}"
            )

            self.configure_dynamic_input(canvas)

            self.set_prompt(
                canvas,
                "Especifique segundo punto del eje:",
            )
            self.show_status(
                canvas,
                "MIRROR: indica el segundo punto o escribe "
                "Distancia y Ángulo",
            )

            canvas.update()
            return

        point = self.apply_ortho(
            canvas,
            point,
        )

        self.complete_mirror(
            canvas,
            point,
        )

    # ---------------------------------------------------------
    # TEXTO
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        value = str(text or "").strip()

        if (
            not value
            or self.axis_start is None
        ):
            return False

        direction_point = (
            self.current_point
            or self.get_canvas_point(canvas)
        )

        try:
            point = CoordinateParser.parse(
                value,
                base_point=self.axis_start,
                direction_point=direction_point,
            )

        except CoordinateParseError as error:
            message = (
                f"MIRROR: entrada no válida: {error}"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        return self.complete_mirror(
            canvas,
            point,
        )

    # ---------------------------------------------------------
    # EJECUCIÓN E HISTORIAL
    # ---------------------------------------------------------

    def axis_is_valid(self, point):
        dx = point.x - self.axis_start.x
        dy = point.y - self.axis_start.y

        return (dx * dx + dy * dy) > 1.0e-12

    def complete_mirror(self, canvas, axis_end):
        if not self.axis_is_valid(axis_end):
            message = (
                "MIRROR: los dos puntos del eje "
                "deben ser diferentes"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        self.axis_end = axis_end

        mirrored_elements = (
            TransformManager.mirror_elements(
                self.elements,
                self.axis_start,
                self.axis_end,
            )
        )

        if (
            mirrored_elements
            and self.app_core is not None
        ):
            self.app_core.history.push(
                MirrorAction(
                    mirrored_elements,
                    self.axis_start,
                    self.axis_end,
                )
            )

        print(
            f"MIRROR: Segundo punto {self.axis_end}"
        )
        print(
            f"MIRROR completado: "
            f"{len(mirrored_elements)} objeto(s)"
        )

        self.finish(canvas)
        return bool(mirrored_elements)

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
        self.axis_start = None
        self.axis_end = None
        self.first_point = None
        self.current_point = None

        self.set_prompt(canvas, "Comando:")
        self.show_status(
            canvas,
            "MIRROR completado",
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
            and self.axis_start is None
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
                "MIRROR cancelado",
            )

        self.elements = []
        self.axis_start = None
        self.axis_end = None
        self.first_point = None
        self.current_point = None

        print("MIRROR finalizado")

    def deactivate(self):
        self.elements = []
        self.axis_start = None
        self.axis_end = None
        self.first_point = None
        self.current_point = None

        print("MIRROR desactivado")
