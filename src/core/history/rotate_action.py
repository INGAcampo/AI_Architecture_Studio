"""
AI Architecture Studio
History - Rotate Action

Foundation 4.2
"""

from core.history.history_action import HistoryAction
from engines.transform.transform_manager import TransformManager


class RotateAction(HistoryAction):

    def __init__(self, elements, angle, cx, cy, cz=0.0):
        self.elements = list(elements)
        self.angle = angle
        self.cx = cx
        self.cy = cy
        self.cz = cz

    def undo(self):
        for element in self.elements:
            TransformManager.rotate_element(
                element,
                -self.angle,
                self.cx,
                self.cy,
                self.cz,
            )

    def redo(self):
        for element in self.elements:
            TransformManager.rotate_element(
                element,
                self.angle,
                self.cx,
                self.cy,
                self.cz,
            )
