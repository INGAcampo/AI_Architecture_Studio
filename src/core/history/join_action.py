"""
AI Architecture Studio
JOIN History Action — Package 4.3
"""

from core.history.history_action import HistoryAction


class JoinAction(HistoryAction):

    def __init__(self, scene, originals, replacement):
        self.scene = scene
        self.originals = list(originals)
        self.replacement = replacement

    def _elements(self):
        getter = getattr(self.scene, "get_elements", None)
        if callable(getter):
            return getter()
        return getattr(self.scene, "elements", [])

    def _remove(self, element):
        try:
            self.scene.remove_element(element)
        except (ValueError, AttributeError):
            pass

    def _add(self, element):
        if element not in self._elements():
            self.scene.add_element(element)

    def undo(self):
        self._remove(self.replacement)
        for element in self.originals:
            self._add(element)

    def redo(self):
        for element in self.originals:
            self._remove(element)
        self._add(self.replacement)
