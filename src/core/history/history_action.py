"""
AI Architecture Studio
History Action

Foundation 3.2
"""


class HistoryAction:

    def undo(self):
        """
        Revierte la acción.
        """
        raise NotImplementedError

    def redo(self):
        """
        Reaplica la acción.
        """
        raise NotImplementedError