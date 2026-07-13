"""
AI Architecture Studio
CAD Command - Scale

Foundation 4.2
"""

from commands.base_command import BaseCommand
from core.history.scale_action import ScaleAction
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class ScaleCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "SCALE"
        self.elements = []
        self.base_point = None
        self.reference_point = None
        self.final_point = None

    def activate(self):
        super().activate()

        print(
            "SCALE activo: selecciona objetos antes de activar "
            "y luego indica punto base, referencia y final"
        )

    def mouse_press(self, event, canvas):
        if not self.elements:
            self.elements = (
                canvas.selection_manager.selected_elements()
            )

            if not self.elements:
                print("SCALE: No hay objetos seleccionados")
                canvas.tool_manager.cancel(canvas)
                return

        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.base_point is None:
            self.base_point = point
            print(f"SCALE: Punto base {point}")
            return

        if self.reference_point is None:
            self.reference_point = point
            print(f"SCALE: Punto referencia {point}")
            return

        self.final_point = point

        reference_distance = self.reference_point.distance_to(self.base_point)
        final_distance = self.final_point.distance_to(self.base_point)

        if reference_distance == 0:
            print("SCALE: Distancia de referencia inválida")
            canvas.tool_manager.cancel(canvas)
            return

        scale_factor = final_distance / reference_distance

        scaled_elements = []

        for element in self.elements:
            scaled = TransformManager.scale_element(
                element,
                scale_factor,
                self.base_point.x,
                self.base_point.y,
                self.base_point.z,
            )

            if scaled:
                scaled_elements.append(element)

        if scaled_elements and self.app_core:
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
            f"SCALE: {len(scaled_elements)} objeto(s) escalados "
            f"factor={scale_factor:.3f}"
        )

        canvas.selection_manager.clear()
        canvas.highlight.clear()
        canvas.element_selected.emit(None)
        canvas.update()

        self.elements = []
        self.base_point = None
        self.reference_point = None
        self.final_point = None

        canvas.tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        self.elements = []
        self.base_point = None
        self.reference_point = None
        self.final_point = None

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("SCALE finalizado")
