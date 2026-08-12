"""
AI Architecture Studio
History Action - TRIM

Professional Package 3.9
"""

from core.history.history_action import HistoryAction


class TrimAction(HistoryAction):
    """
    Sustituye un objeto original por sus geometrías recortadas.
    """

    def __init__(self, scene, original, replacements):
        self.scene = scene
        self.original = original
        self.replacements = list(replacements or [])

    def undo(self):
        for element in reversed(self.replacements):
            self.scene.remove_element(element)

        if self.original not in self.scene.elements:
            self.scene.add_element(self.original)

    def redo(self):
        self.scene.remove_element(self.original)

        for element in self.replacements:
            if element not in self.scene.elements:
                self.scene.add_element(element)
