"""
AI Architecture Studio
CAD Command - Rectangle

Foundation 3.4
"""

from commands.base_command import BaseCommand
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class RectangleCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "RECTANGLE"
        self.first_corner = None

    def mouse_press(self, event, canvas):
        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.first_corner is None:
            self.first_corner = point
            print(f"RECTANGLE: Primera esquina {point}")
            return

        rectangle = GeometryBuilder.create_rectangle(
            self.first_corner,
            point
        )

        canvas.scene.add_element(rectangle)

        if self.app_core:
            from core.history.add_action import AddAction

            self.app_core.history.push(
                AddAction(canvas.scene, rectangle)
            )

        print("RECTANGLE creado")

        self.first_corner = None
        canvas.preview_geometry = None
        canvas.update()

        # Finalizar herramienta y volver al modo selección
        canvas.tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        self.first_corner = None

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("RECTANGLE finalizado")