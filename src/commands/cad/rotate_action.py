import math

from engines.transform.transform_manager import TransformManager


class RotateAction:

    def __init__(
        self,
        elements,
        angle_degrees,
        cx,
        cy,
        cz=0.0,
    ):
        self.elements = list(elements or [])
        self.angle_degrees = angle_degrees
        self.cx = cx
        self.cy = cy
        self.cz = cz

    def undo(self):
        TransformManager.rotate_elements(
            self.elements,
            math.radians(-self.angle_degrees),
            self.cx,
            self.cy,
            self.cz,
        )

    def redo(self):
        TransformManager.rotate_elements(
            self.elements,
            math.radians(self.angle_degrees),
            self.cx,
            self.cy,
            self.cz,
        )
