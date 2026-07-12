"""
AI Architecture Studio
CAD Command - Line Profesional

Foundation 3.2
"""

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point
from models.cad_line import CadLine


class LineCommand(BaseCommand):
    def __init__(self, app_core=None):
        super().__init__(app_core)
        self.name = "LINE"
        self.first_point = None

    def mouse_move(self, event, canvas):
        if self.first_point is None:
            canvas.preview_geometry = None
            return

        x, y = canvas.cursor_position
        current_point = Point(x, y, 0)

        canvas.preview_geometry = GeometryBuilder.create_line(
            self.first_point,
            current_point,
        )

        canvas.update()

    def mouse_press(self, event, canvas):
        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        if self.first_point is None:
            self.first_point = point
            print(f"LINE: Primer punto {point}")
            return

        line = GeometryBuilder.create_line(
            self.first_point,
            point,
        )

        cad_line = CadLine(line)
        canvas.scene.add_element(cad_line)

        if self.app_core:
            self.app_core.history.push(
                AddAction(canvas.scene, cad_line)
            )

        print(f"LINE creada: {line}")

        self.first_point = None
        canvas.preview_geometry = None
        canvas.update()

    def cancel(self, canvas=None):
        self.first_point = None

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("LINE cancelada")

    def deactivate(self):
        self.first_point = None
        print("Comando LINE desactivado")