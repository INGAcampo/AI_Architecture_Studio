"""
AI Architecture Studio
CAD Command - TRIM Profesional

Package 3.9.1
Corrección de resaltado, persistencia y mensajes repetidos.
"""

from commands.base_command import BaseCommand
from core.history.trim_action import TrimAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class TrimCommand(BaseCommand):

    PICK_TOLERANCE = 0.40

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "TRIM"
        self.cutting_elements = []

        # Evita que mouseMoveEvent repita indefinidamente
        # "No hay bordes de corte seleccionados".
        self.selection_checked = False
        self.missing_selection_reported = False

    def activate(self):
        super().activate()

        print(
            "TRIM activo: usa los objetos preseleccionados "
            "como bordes de corte y haz clic sobre el tramo "
            "que deseas eliminar"
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

    def capture_cutting_edges(self, canvas):
        """
        Captura una sola vez los bordes preseleccionados y los
        conserva durante toda la sesión TRIM.
        """
        if self.cutting_elements:
            return True

        if self.selection_checked:
            return False

        self.selection_checked = True

        selected = (
            canvas.selection_manager
            .selected_elements()
        )

        self.cutting_elements = [
            element
            for element in selected
            if GeometryBuilder.can_be_cutting_edge(element)
        ]

        if not self.cutting_elements:
            if not self.missing_selection_reported:
                print(
                    "TRIM: No hay bordes de corte seleccionados"
                )
                self.missing_selection_reported = True

            self.set_prompt(
                canvas,
                "Preseleccione bordes y active TRIM nuevamente:",
            )
            self.show_status(
                canvas,
                "TRIM: preselecciona uno o varios bordes "
                "de corte antes de activar el comando",
            )
            return False

        print(
            f"TRIM: {len(self.cutting_elements)} borde(s) "
            "de corte"
        )

        # No vaciamos selection_manager: los bordes quedan
        # disponibles durante toda la sesión del comando.
        canvas.highlight.clear()
        canvas.update()

        self.set_prompt(
            canvas,
            "Seleccione tramo a recortar:",
        )
        self.show_status(
            canvas,
            "TRIM: haz clic en el tramo que deseas eliminar",
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
            if element in self.cutting_elements:
                continue

            if not GeometryBuilder.can_trim_element(element):
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
        if not self.capture_cutting_edges(canvas):
            return

        point = self.get_canvas_point(canvas)
        target = self.find_target(canvas, point)

        canvas.highlight.clear()

        if target is not None:
            # Highlight usa set(), no add().
            canvas.highlight.set(target)

        canvas.update()

    def mouse_press(self, event, canvas):
        if not self.capture_cutting_edges(canvas):
            # Un solo clic finaliza limpiamente cuando TRIM fue
            # activado sin bordes preseleccionados.
            canvas.tool_manager.cancel(canvas)
            return

        point = self.get_canvas_point(canvas)
        target = self.find_target(canvas, point)

        if target is None:
            message = (
                "TRIM: No se encontró un tramo compatible "
                "cerca del cursor"
            )
            print(message)
            self.show_status(
                canvas,
                "TRIM: acerca el cursor a una LINE, PLINE "
                "o RECTANGLE",
            )
            return

        replacements = GeometryBuilder.trim_element(
            target,
            self.cutting_elements,
            point,
        )

        if replacements is None:
            message = (
                "TRIM: el tramo señalado ya termina en el borde "
                "o no lo intersecta"
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
            print("TRIM: escena no disponible")
            return

        scene.remove_element(target)

        for element in replacements:
            scene.add_element(element)

        if self.app_core is not None:
            self.app_core.history.push(
                TrimAction(
                    scene,
                    target,
                    replacements,
                )
            )

        print(
            f"TRIM completado: 1 objeto modificado, "
            f"{len(replacements)} segmento(s) resultante(s)"
        )

        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self.show_status(
            canvas,
            "TRIM completado: selecciona otro tramo "
            "o presiona ESC",
        )

    # ---------------------------------------------------------
    # TECLADO Y FINALIZACIÓN
    # ---------------------------------------------------------

    def handle_text_input(self, text, canvas):
        command = str(text or "").strip().upper()

        if command in {"", "ENTER"}:
            return self.capture_cutting_edges(canvas)

        return False

    def cancel(self, canvas=None):
        self.cutting_elements = []
        self.selection_checked = False
        self.missing_selection_reported = False

        if canvas is not None:
            canvas.preview_geometry = None
            canvas.highlight.clear()
            canvas.update()

            self.set_prompt(canvas, "Comando:")
            self.show_status(canvas, "TRIM cancelado")

        print("TRIM finalizado")

    def deactivate(self):
        self.cutting_elements = []
        self.selection_checked = False
        self.missing_selection_reported = False

        print("TRIM desactivado")
