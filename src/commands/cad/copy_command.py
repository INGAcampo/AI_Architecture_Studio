"""
AI Architecture Studio
CAD Command - Copy

Foundation 4.2
"""

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class CopyCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "COPY"
        self.elements = []
        self.base_point = None

    def activate(self):
        super().activate()

        print(
            "COPY activo: selecciona objetos antes de activar "
            "el comando y luego indica punto base y destino"
        )

    def mouse_press(self, event, canvas):
        if not self.elements:
            self.elements = (
                canvas.selection_manager.selected_elements()
            )

            if not self.elements:
                print("COPY: No hay objetos seleccionados")
                canvas.tool_manager.cancel(canvas)
                return

        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.base_point is None:
            self.base_point = point
            print(f"COPY: Punto base {point}")
            return

        dx = point.x - self.base_point.x
        dy = point.y - self.base_point.y
        dz = point.z - self.base_point.z

        copied_elements = []

        for element in self.elements:
            clone_method = getattr(element, "clone", None)

            if not callable(clone_method):
                print(
                    f"COPY: {element.__class__.__name__} "
                    "no admite clonación"
                )
                continue

            copied_element = clone_method()

            moved = TransformManager.move_element(
                copied_element,
                dx,
                dy,
                dz,
            )

            if not moved:
                print(
                    f"COPY: No se pudo desplazar "
                    f"{element.__class__.__name__}"
                )
                continue

            canvas.scene.add_element(copied_element)
            copied_elements.append(copied_element)

            if self.app_core:
                self.app_core.history.push(
                    AddAction(
                        canvas.scene,
                        copied_element,
                    )
                )

        print(
            f"COPY: {len(copied_elements)} objeto(s) copiados "
            f"dx={dx:.3f}, dy={dy:.3f}"
        )

        canvas.selection_manager.clear()
        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self.elements = []
        self.base_point = None

        canvas.tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        self.elements = []
        self.base_point = None

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("COPY finalizado")