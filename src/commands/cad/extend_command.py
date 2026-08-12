"""
AI Architecture Studio
CAD Command - EXTEND Profesional

Package 4.0
"""

from commands.base_command import BaseCommand
from core.history.extend_action import ExtendAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class ExtendCommand(BaseCommand):

    PICK_TOLERANCE = 0.40

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "EXTEND"
        self.boundary_elements = []
        self.selection_checked = False
        self.missing_selection_reported = False

    def activate(self):
        super().activate()

        print(
            "EXTEND activo: usa los objetos preseleccionados "
            "como límites y haz clic cerca del extremo "
            "que deseas extender"
        )

    # ---------------------------------------------------------
    # UTILIDADES
    # ---------------------------------------------------------

    def get_canvas_point(self, canvas):
        getter = getattr(canvas, "get_input_point", None)

        if callable(getter):
            return getter()

        x, y = canvas.cursor_position
        return Point(x, y, 0.0)

    def get_main_window(self, canvas):
        getter = getattr(canvas, "window", None)

        if not callable(getter):
            return None

        return getter()

    def set_prompt(self, canvas, text):
        window = self.get_main_window(canvas)

        if window is None:
            return

        command_line = getattr(window, "command_line", None)

        if command_line is not None:
            command_line.set_prompt(text)

    def show_status(self, canvas, text):
        window = self.get_main_window(canvas)

        if (
            window is not None
            and hasattr(window, "statusBar")
        ):
            window.statusBar().showMessage(text)

    def capture_boundaries(self, canvas):
        """
        Captura una sola vez los límites preseleccionados y los
        conserva durante toda la sesión EXTEND.
        """
        if self.boundary_elements:
            return True

        if self.selection_checked:
            return False

        self.selection_checked = True

        selected = (
            canvas.selection_manager
            .selected_elements()
        )

        self.boundary_elements = [
            element
            for element in selected
            if GeometryBuilder.can_be_extension_boundary(element)
        ]

        if not self.boundary_elements:
            if not self.missing_selection_reported:
                print(
                    "EXTEND: No hay límites seleccionados"
                )
                self.missing_selection_reported = True

            self.set_prompt(
                canvas,
                "Preseleccione límites y active EXTEND nuevamente:",
            )
            self.show_status(
                canvas,
                "EXTEND: preselecciona uno o varios límites "
                "antes de activar el comando",
            )
            return False

        print(
            f"EXTEND: {len(self.boundary_elements)} "
            "límite(s)"
        )

        canvas.highlight.clear()
        canvas.update()

        self.set_prompt(
            canvas,
            "Seleccione extremo a extender:",
        )
        self.show_status(
            canvas,
            "EXTEND: haz clic cerca del extremo "
            "de una línea",
        )

        return True

    def find_target(self, canvas, point):
        scene = getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

        if scene is None:
            return None

        candidates = []

        for element in scene.elements:
            if element in self.boundary_elements:
                continue

            if not GeometryBuilder.can_extend_element(element):
                continue

            distance = GeometryBuilder.distance_to_element(
                element,
                point,
            )

            candidates.append(
                (distance, element)
            )

        if not candidates:
            return None

        distance, element = min(
            candidates,
            key=lambda item: item[0],
        )

        if distance > self.PICK_TOLERANCE:
            return None

        return element

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if not self.capture_boundaries(canvas):
            return

        point = self.get_canvas_point(canvas)
        target = self.find_target(canvas, point)

        canvas.highlight.clear()

        if target is not None:
            canvas.highlight.set(target)

        canvas.update()

    def mouse_press(self, event, canvas):
        if not self.capture_boundaries(canvas):
            canvas.tool_manager.cancel(canvas)
            return

        point = self.get_canvas_point(canvas)
        target = self.find_target(canvas, point)

        if target is None:
            message = (
                "EXTEND: No se encontró una línea compatible "
                "cerca del cursor"
            )
            print(message)
            self.show_status(canvas, message)
            return

        replacement = GeometryBuilder.extend_element(
            target,
            self.boundary_elements,
            point,
        )

        if replacement is None:
            message = (
                "EXTEND: el extremo señalado no alcanza "
                "ninguno de los límites seleccionados"
            )
            print(message)
            self.show_status(canvas, message)
            return

        scene = getattr(
            self.app_core,
            "scene",
            getattr(canvas, "scene", None),
        )

        if scene is None:
            print("EXTEND: escena no disponible")
            return

        scene.remove_element(target)
        scene.add_element(replacement)

        if self.app_core is not None:
            self.app_core.history.push(
                ExtendAction(
                    scene,
                    target,
                    replacement,
                )
            )

        print(
            "EXTEND completado: 1 objeto extendido"
        )

        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self.show_status(
            canvas,
            "EXTEND completado: selecciona otro extremo "
            "o presiona ESC",
        )

    # ---------------------------------------------------------
    # TECLADO Y FINALIZACIÓN
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        command = str(text or "").strip().upper()

        if command in {"", "ENTER"}:
            return self.capture_boundaries(canvas)

        return False

    def cancel(self, canvas=None):
        self.boundary_elements = []
        self.selection_checked = False
        self.missing_selection_reported = False

        if canvas is not None:
            canvas.preview_geometry = None
            canvas.highlight.clear()
            canvas.update()

            self.set_prompt(canvas, "Comando:")
            self.show_status(canvas, "EXTEND cancelado")

        print("EXTEND finalizado")

    def deactivate(self):
        self.boundary_elements = []
        self.selection_checked = False
        self.missing_selection_reported = False

        print("EXTEND desactivado")
