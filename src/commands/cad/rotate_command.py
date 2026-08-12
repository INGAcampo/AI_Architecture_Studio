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
        self.first_point = None

    def activate(self):
        super().activate()
        print(
            "ROTATE activo: selecciona objetos, "
            "indica el centro y escribe el ángulo"
        )

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

    def mouse_press(self, event, canvas):

        if not self.elements:
            self.elements = [
                e for e in
                canvas.selection_manager.selected_elements()
                if TransformManager.can_rotate_element(e)
            ]

        if not self.elements:
            print("ROTATE: no hay selección")
            return

        if self.base_point is None:
            self.base_point = self.get_canvas_point(canvas)
            self.first_point = self.base_point

            print(
                f"ROTATE: Centro {self.base_point}"
            )

    def handle_text_input(self, text, canvas):

        if self.base_point is None:
            return False

        angle_degrees = float(
            str(text).replace(",", ".")
        )

        rotated = TransformManager.rotate_elements(
            self.elements,
            math.radians(angle_degrees),
            self.base_point.x,
            self.base_point.y,
            self.base_point.z,
        )

        if rotated and self.app_core is not None:
            self.app_core.history.push(
                RotateAction(
                    rotated,
                    angle_degrees,
                    self.base_point.x,
                    self.base_point.y,
                    self.base_point.z,
                )
            )

        print(
            f"ROTATE completado: "
            f"{len(rotated)} objeto(s), "
            f"ángulo={angle_degrees}°"
        )

        canvas.update()

        tool_manager = getattr(
            canvas,
            "tool_manager",
            None,
        )

        if tool_manager is not None:
            tool_manager.cancel(canvas)

        return True
