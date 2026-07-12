"""
AI Architecture Studio
History - Delete Action

Foundation 3.2
"""

from core.history.history_action import HistoryAction


class DeleteAction(HistoryAction):

    def __init__(self, scene, element):
        self.scene = scene
        self.element = element

    def undo(self):
        self.scene.add_element(self.element)

    def redo(self):
        self.scene.remove_element(self.element)