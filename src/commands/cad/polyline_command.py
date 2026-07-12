"""
AI Architecture Studio
CAD Command - Polyline

Foundation 3.4
"""

from PySide6.QtCore import Qt

from commands.base_command import BaseCommand
from core.history.add_action import AddAction
from engines.geometry.geometry_builder import GeometryBuilder
from engines.geometry.point import Point


class PolylineCommand(BaseCommand):

    def __init__(self, app_core=None):
        super().__init__(app_core)

        self.name = "PLINE"
        self.points = []

    def mouse_move(self, event, canvas):
        if not self.points:
            canvas.preview_geometry = None
            return

        x, y = canvas.cursor_position
        current_point = Point(x, y, 0)

        canvas.preview_geometry = GeometryBuilder.create_line(
            self.points[-1],
            current_point
        )

        canvas.update()

    def mouse_press(self, event, canvas):
        x, y = canvas.cursor_position
        point = Point(x, y, 0)

        self.points.append(point)

        print(f"PLINE: Punto {len(self.points)}")

    def key_press(self, event, canvas):
        if event.key() not in (Qt.Key_Return, Qt.Key_Enter):
            return

        if len(self.points) >= 2:
            polyline = GeometryBuilder.create_polyline(
                self.points,
                closed=False
            )

            canvas.scene.add_element(polyline)

            if self.app_core:
                self.app_core.history.push(
                    AddAction(canvas.scene, polyline)
                )

            print(
                f"PLINE creada con {len(self.points)} puntos"
            )

        self.points = []
        canvas.preview_geometry = None
        canvas.update()

        # Finalizar herramienta y volver al modo selección
        canvas.tool_manager.cancel(canvas)

    def cancel(self, canvas=None):
        self.points = []

        if canvas:
            canvas.preview_geometry = None
            canvas.update()

        print("PLINE finalizada")