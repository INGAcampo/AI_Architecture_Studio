"""
AI Architecture Studio
History Action — CHAMFER Professional 4.2
"""

from core.history.history_action import HistoryAction


class ChamferAction(HistoryAction):

    def __init__(self, scene, originals, replacements):
        self.scene = scene
        self.originals = list(originals)
        self.replacements = list(replacements)

    def _remove(self, elements):
        for element in elements:
            try:
                self.scene.remove_element(element)
            except (ValueError, AttributeError):
                pass

    def _add(self, elements):
        current = getattr(self.scene, "elements", [])

        for element in elements:
            if element not in current:
                self.scene.add_element(element)

    def undo(self):
        self._remove(self.replacements)
        self._add(self.originals)

    def redo(self):
        self._remove(self.originals)
        self._add(self.replacements)
