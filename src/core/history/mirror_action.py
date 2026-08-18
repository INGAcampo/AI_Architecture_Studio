"""
AI Architecture Studio
History Action - Mirror

Dynamic Input Universal - Package 3.7
"""

from core.history.history_action import HistoryAction
from engines.transform.transform_manager import TransformManager


class MirrorAction(HistoryAction):
    """
    Acción reversible de simetría.

    MIRROR es una transformación involutiva: aplicar la misma
    reflexión dos veces restaura exactamente la geometría original.
    """

    def __init__(
        self,
        elements,
        axis_start,
        axis_end,
    ):
        self.elements = list(elements or [])
        self.axis_start = axis_start
        self.axis_end = axis_end

    def undo(self):
        TransformManager.mirror_elements(
            self.elements,
            self.axis_start,
            self.axis_end,
        )

    def redo(self):
        TransformManager.mirror_elements(
            self.elements,
            self.axis_start,
            self.axis_end,
        )
