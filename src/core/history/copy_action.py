"""
AI Architecture Studio
History Action - Copy

Dynamic Input Universal - Package 3.4
"""

from core.history.history_action import HistoryAction


class CopyAction(HistoryAction):
    """
    Acción reversible para una operación COPY múltiple.

    Las copias ya deben estar insertadas en la escena cuando
    esta acción se registra en HistoryManager.
    """

    def __init__(self, scene, copied_elements):
        self.scene = scene
        self.copied_elements = list(copied_elements or [])

    def undo(self):
        for element in reversed(self.copied_elements):
            self.scene.remove_element(element)

    def redo(self):
        for element in self.copied_elements:
            self.scene.add_element(element)
