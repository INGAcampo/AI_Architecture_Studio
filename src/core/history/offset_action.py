"""
AI Architecture Studio
History Action - Offset

Dynamic Input Universal - Package 3.8
"""

from core.history.history_action import HistoryAction


class OffsetAction(HistoryAction):
    """
    Acción reversible para objetos creados por OFFSET.
    """

    def __init__(self, scene, elements):
        self.scene = scene
        self.elements = list(elements or [])

    def undo(self):
        for element in reversed(self.elements):
            self.scene.remove_element(element)

    def redo(self):
        for element in self.elements:
            if element not in self.scene.elements:
                self.scene.add_element(element)
