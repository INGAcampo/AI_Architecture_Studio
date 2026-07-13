"""
AI Architecture Studio
CAD Command - Rotate

Foundation 4.2
"""

import math

from commands.base_command import BaseCommand
from core.history.rotate_action import RotateAction
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class RotateCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "ROTATE"
        self.elements = []
        self.base_point = None

    def activate(self):
        super().activate()

        print(
            "ROTATE activo: selecciona objetos antes de activar "
            "y luego indica un punto base y un ángulo"
        )

    def mouse_press(self, event, canvas):
        if not self.elements:
            self.elements = (
                canvas.selection_manager.selected_elements()
            )

            if not self.elements:
                print("ROTATE: No hay objetos seleccionados")
                canvas.tool_manager.cancel(canvas)
                return

        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.base_point is None:
            self.base_point = point
            print(f"ROTATE: Punto base {point}")
            return

        angle = math.atan2(
            point.y - self.base_point.y,
            point.x - self.base_point.x,
        )

        rotated_elements = []

        for element in self.elements:
            rotated = TransformManager.rotate_element(
                element,
                angle,
                self.base_point.x,
                self.base_point.y,
                self.base_point.z,
            )

            if rotated:
                rotated_elements.append(element)

        if rotated_elements and self.app_core:
            self.app_core.history.push(
                RotateAction(
                    rotated_elements,
                    angle,
                    self.base_point.x,
                    self.base_point.y,
                    self.base_point.z,
                )
            )

        print(
            f"ROTATE: {len(rotated_elements)} objeto(s) rotados "
            f"angle={angle:.3f}"
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

        print("ROTATE finalizado")
