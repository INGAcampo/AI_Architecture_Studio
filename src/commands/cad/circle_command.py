"""
AI Architecture Studio
CAD Command - Circle

Foundation 3.4
"""

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.geometry.point import Point
from models.cad_circle import CadCircle


class CircleCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "CIRCLE"
        self.center = None

    def mouse_press(self, event, canvas):
        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.center is None:
            self.center = point
            print(f"CIRCLE: Centro {point}")
            return

        radius = self.center.distance_to(point)

        if radius <= 0:
            print("CIRCLE: Radio inválido")
            return

        circle = CadCircle(
            center=self.center,
            radius=radius
        )

        canvas.scene.add_element(circle)

        if self.app_core:
            self.app_core.history.push(
                AddAction(canvas.scene, circle)
            )

        print(
            f"CIRCLE creado: centro={self.center}, "
            f"radio={radius:.3f}"
        )

        self.center = None
        canvas.preview_geometry = None
        canvas.update()

        # Finalizar herramienta y volver al modo selección
        canvas.tool_manager.cancel(canvas)

    def mouse_move(self, event, canvas):
        if self.center is None:
            canvas.preview_geometry = None
            return

        x, y = canvas.cursor_position
        current_point = Point(x, y, 0)

        canvas.preview_geometry = CadCircle(
            center=self.center,
            radius=self.center.distance_to(current_point)
        )

        canvas.update()

    def cancel(self, canvas=None):
        self.center = None

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("CIRCLE finalizado")