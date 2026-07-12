"""
AI Architecture Studio
History - Move Action

Foundation 3.5
"""

from core.history.history_action import HistoryAction
from engines.transform.transform_manager import TransformManager


class MoveAction(HistoryAction):

    def __init__(self, elements, dx, dy, dz=0.0):
        self.elements = list(elements)
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def undo(self):
        for element in self.elements:
            TransformManager.move_element(
                element,
                -self.dx,
                -self.dy,
                -self.dz,
            )

    def redo(self):
        for element in self.elements:
            TransformManager.move_element(
                element,
                self.dx,
                self.dy,
                self.dz,
            )