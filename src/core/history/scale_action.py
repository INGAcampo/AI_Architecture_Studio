"""
AI Architecture Studio
History Action - Scale

Dynamic Input Universal - Package 3.6
"""

from core.history.history_action import HistoryAction
from engines.transform.transform_manager import TransformManager


class ScaleAction(HistoryAction):
    """
    Acción reversible para SCALE.

    Los objetos ya están escalados cuando esta acción se
    registra en HistoryManager.
    """

    def __init__(
        self,
        elements,
        scale_factor,
        cx,
        cy,
        cz=0.0,
    ):
        self.elements = list(elements or [])
        self.scale_factor = float(scale_factor)
        self.cx = float(cx)
        self.cy = float(cy)
        self.cz = float(cz)

    def undo(self):
        TransformManager.scale_elements(
            self.elements,
            1.0 / self.scale_factor,
            self.cx,
            self.cy,
            self.cz,
        )

    def redo(self):
        TransformManager.scale_elements(
            self.elements,
            self.scale_factor,
            self.cx,
            self.cy,
            self.cz,
        )
