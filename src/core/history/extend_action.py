"""
AI Architecture Studio
History Action - EXTEND

Professional Package 4.0
"""

from core.history.history_action import HistoryAction


class ExtendAction(HistoryAction):
    """
    Sustituye una geometría original por su versión extendida.
    """

    def __init__(self, scene, original, replacement):
        self.scene = scene
        self.original = original
        self.replacement = replacement

    def undo(self):
        self.scene.remove_element(self.replacement)

        if self.original not in self.scene.elements:
            self.scene.add_element(self.original)

    def redo(self):
        self.scene.remove_element(self.original)

        if self.replacement not in self.scene.elements:
            self.scene.add_element(self.replacement)
