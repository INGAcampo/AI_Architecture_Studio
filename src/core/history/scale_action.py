"""
AI Architecture Studio
History - Scale Action

Foundation 4.2
"""

from core.history.history_action import HistoryAction
from engines.transform.transform_manager import TransformManager


class ScaleAction(HistoryAction):

    def __init__(self, elements, scale_factor, cx, cy, cz=0.0):
        self.elements = list(elements)
        self.scale_factor = scale_factor
        self.cx = cx
        self.cy = cy
        self.cz = cz

    def undo(self):
        inverse_factor = 1.0 / self.scale_factor if self.scale_factor else 1.0

        for element in self.elements:
            TransformManager.scale_element(
                element,
                inverse_factor,
                self.cx,
                self.cy,
                self.cz,
            )

    def redo(self):
        for element in self.elements:
            TransformManager.scale_element(
                element,
                self.scale_factor,
                self.cx,
                self.cy,
                self.cz,
            )
