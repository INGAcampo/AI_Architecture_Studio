"""
AI Architecture Studio
CAD Command - Move

Foundation 3.5
"""

from commands.base_command import BaseCommand
from core.history.move_action import MoveAction
from engines.geometry.point import Point
from engines.transform.transform_manager import TransformManager


class MoveCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "MOVE"
        self.elements = []
        self.base_point = None

    def activate(self):
        super().activate()

        print(
            "MOVE activo: selecciona objetos antes de activar "
            "el comando y luego indica punto base y destino"
        )

    def mouse_press(self, event, canvas):
        if not self.elements:
            self.elements = (
                canvas.selection_manager.selected_elements()
            )

            if not self.elements:
                print("MOVE: No hay objetos seleccionados")
                canvas.tool_manager.cancel(canvas)
                return

        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.base_point is None:
            self.base_point = point
            print(f"MOVE: Punto base {point}")
            return

        dx = point.x - self.base_point.x
        dy = point.y - self.base_point.y
        dz = point.z - self.base_point.z

        moved_elements = []

        for element in self.elements:
            moved = TransformManager.move_element(
                element,
                dx,
                dy,
                dz
            )

            if moved:
                moved_elements.append(element)

        if moved_elements and self.app_core:
            self.app_core.history.push(
                MoveAction(
                    moved_elements,
                    dx,
                    dy,
                    dz
                )
            )

        print(
            f"MOVE: {len(moved_elements)} objeto(s) movidos "
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

        print("MOVE finalizado")