"""
AI Architecture Studio
CAD Command - Line Profesional

Foundation 4.3
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

    def get_ortho_manager(self, canvas):
        scene = getattr(canvas, "scene", None)
        kernel = getattr(scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get("ortho_manager")

    def apply_ortho(self, canvas, point):
        if self.first_point is None:
            return point

        ortho_manager = self.get_ortho_manager(canvas)

        if ortho_manager is None:
            return point

        return ortho_manager.apply(
            self.first_point,
            point,
        )

    def mouse_move(self, event, canvas):
        if self.first_point is None:
            canvas.preview_geometry = None
            canvas.update()
            return

        x, y = canvas.cursor_position

        current_point = Point(
            x,
            y,
            0,
        )

        current_point = self.apply_ortho(
            canvas,
            current_point,
        )

        canvas.preview_geometry = GeometryBuilder.create_line(
            self.first_point,
            current_point,
        )

        canvas.update()

    def mouse_press(self, event, canvas):
        x, y = canvas.cursor_position

        point = Point(
            x,
            y,
            0,
        )

        if self.first_point is None:
            self.first_point = point

            print(
                f"LINE: Primer punto {point}"
            )

            return

        point = self.apply_ortho(
            canvas,
            point,
        )

        if point.distance_to(self.first_point) <= 1e-9:
            print(
                "LINE: El segundo punto debe ser "
                "distinto del primero"
            )
            return

        line = GeometryBuilder.create_line(
            self.first_point,
            point,
        )

        cad_line = CadLine(line)

        canvas.scene.add_element(cad_line)

        if self.app_core:
            self.app_core.history.push(
                AddAction(
                    canvas.scene,
                    cad_line,
                )
            )

        print(
            f"LINE creada: {line}"
        )

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

        print(
            "Comando LINE desactivado"
        )