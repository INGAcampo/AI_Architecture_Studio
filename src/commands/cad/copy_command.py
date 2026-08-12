"""
AI Architecture Studio
CAD Command - Copy Profesional

Dynamic Input Universal - Package 3.4
"""

from commands.base_command import BaseCommand
from core.history.copy_action import CopyAction
from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class CopyCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "COPY"

        self.elements = []
        self.base_point = None

        # Canvas activa el Dynamic Input cuando first_point
        # contiene el punto base.
        self.first_point = None

        self.current_target = None

    # ---------------------------------------------------------
    # ACTIVACIÓN Y SERVICIOS
    # ---------------------------------------------------------

    def activate(self):
        super().activate()

        print(
            "COPY activo: selecciona uno o varios objetos, "
            "indica el punto base y luego el destino"
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

    def get_scene(self, canvas):
        scene = getattr(canvas, "scene", None)

        if scene is not None:
            return scene

        if self.app_core is not None:
            return getattr(
                self.app_core,
                "scene",
                None,
            )

        return None

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
            if TransformManager.can_move_element(element)
            and callable(getattr(element, "clone", None))
        ]

        if not self.elements:
            print("COPY: No hay objetos compatibles seleccionados")
            self.show_status(
                canvas,
                "COPY: selecciona al menos un objeto "
                "compatible antes de activar el comando",
            )
            return False

        print(
            f"COPY: {len(self.elements)} objeto(s) "
            "seleccionado(s)"
        )

        return True

    # ---------------------------------------------------------
    # RESTRICCIONES Y DYNAMIC INPUT
    # ---------------------------------------------------------

    def apply_ortho(self, canvas, point):
        if self.base_point is None:
            return point

        ortho = self.get_ortho_manager(canvas)

        if (
            ortho is None
            or not getattr(ortho, "enabled", False)
        ):
            return point

        return ortho.apply(
            self.base_point,
            point,
        )

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
            "Distancia / Ángulo"
        )
        manager.show()

    def update_dynamic_preview(
        self,
        canvas,
        point,
    ):
        point = self.apply_ortho(
            canvas,
            point,
        )

        manager = self.get_dynamic_input_manager(
            canvas
        )

        if manager is not None:
            manager.set_base_point(
                self.base_point
            )
            manager.update_point(point)

            point = manager.constrained_point(
                self.base_point
            )

        self.current_target = point

        # Vista previa segura: vector del desplazamiento.
        canvas.preview_geometry = (
            GeometryBuilder.create_line(
                self.base_point,
                point,
            )
        )

        canvas.update()

    # ---------------------------------------------------------
    # RATÓN
    # ---------------------------------------------------------

    def mouse_move(self, event, canvas):
        if self.base_point is None:
            return

        point = self.get_canvas_point(canvas)

        self.update_dynamic_preview(
            canvas,
            point,
        )

    def mouse_press(self, event, canvas):
        if not self.capture_selection(canvas):
            canvas.tool_manager.cancel(canvas)
            return

        point = self.get_canvas_point(canvas)

        if self.base_point is None:
            self.base_point = point
            self.first_point = point
            self.current_target = point

            print(f"COPY: Punto base {point}")

            self.configure_dynamic_input(canvas)

            self.set_prompt(
                canvas,
                "Especifique punto de destino:",
            )
            self.show_status(
                canvas,
                "COPY: indica el destino o escribe "
                "Distancia y Ángulo",
            )

            canvas.update()
            return

        point = self.apply_ortho(
            canvas,
            point,
        )

        self.complete_copy(
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
            or self.base_point is None
        ):
            return False

        direction_point = (
            self.current_target
            or self.get_canvas_point(canvas)
        )

        try:
            point = CoordinateParser.parse(
                value,
                base_point=self.base_point,
                direction_point=direction_point,
            )

        except CoordinateParseError as error:
            message = f"COPY: entrada no válida: {error}"
            print(message)
            self.show_status(canvas, message)
            return False

        return self.complete_copy(
            canvas,
            point,
        )

    # ---------------------------------------------------------
    # CLONACIÓN, ESCENA E HISTORIAL
    # ---------------------------------------------------------

    @staticmethod
    def copy_common_attributes(source, clone):
        """
        Conserva atributos CAD comunes sin copiar el identificador
        interno del objeto original.
        """
        for attribute_name in (
            "layer_name",
            "color",
            "lineweight",
            "linetype",
            "visible",
        ):
            if hasattr(source, attribute_name):
                setattr(
                    clone,
                    attribute_name,
                    getattr(source, attribute_name),
                )

    def create_copies(self, dx, dy, dz):
        copied_elements = []

        for source in self.elements:
            clone_method = getattr(
                source,
                "clone",
                None,
            )

            if not callable(clone_method):
                continue

            clone = clone_method()

            self.copy_common_attributes(
                source,
                clone,
            )

            if TransformManager.move_element(
                clone,
                dx,
                dy,
                dz,
            ):
                copied_elements.append(clone)

        return copied_elements

    def complete_copy(self, canvas, target):
        if (
            self.base_point is None
            or not self.elements
        ):
            return False

        dx = target.x - self.base_point.x
        dy = target.y - self.base_point.y
        dz = target.z - self.base_point.z

        if (
            abs(dx) <= 1e-12
            and abs(dy) <= 1e-12
            and abs(dz) <= 1e-12
        ):
            message = (
                "COPY: el desplazamiento debe ser "
                "distinto de cero"
            )
            print(message)
            self.show_status(canvas, message)
            return False

        scene = self.get_scene(canvas)

        if scene is None:
            message = "COPY: no se encontró SceneManager"
            print(message)
            self.show_status(canvas, message)
            return False

        copied_elements = self.create_copies(
            dx,
            dy,
            dz,
        )

        for source, copied in zip(
            self.elements,
            copied_elements,
        ):
            original_layer = getattr(
                source,
                "layer_name",
                None,
            )

            scene.add_element(copied)

            # SceneManager asigna la capa actual al insertar.
            # COPY debe conservar la capa del objeto original.
            if original_layer is not None:
                copied.layer_name = original_layer

        if (
            copied_elements
            and self.app_core is not None
        ):
            self.app_core.history.push(
                CopyAction(
                    scene,
                    copied_elements,
                )
            )

        print(
            f"COPY completado: "
            f"{len(copied_elements)} objeto(s), "
            f"dx={dx:.6g}, dy={dy:.6g}, dz={dz:.6g}"
        )

        self.finish(canvas)
        return bool(copied_elements)

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
        self.current_target = None

        self.set_prompt(canvas, "Comando:")
        self.show_status(
            canvas,
            "COPY completado",
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
        # ToolManager puede volver a llamar cancel() tras finish().
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
                "COPY cancelado",
            )

        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_target = None

        print("COPY finalizado")

    def deactivate(self):
        self.elements = []
        self.base_point = None
        self.first_point = None
        self.current_target = None

        print("Comando COPY desactivado")
