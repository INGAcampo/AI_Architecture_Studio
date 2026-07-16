"""
AI Architecture Studio
History Action - Grip Edit

Professional Grips v1
"""

from engines.selection.grip_editor import GripEditor


class GripEditAction:

    def __init__(
        self,
        owner,
        before_state,
        after_state,
    ):
        self.owner = owner
        self.before_state = before_state
        self.after_state = after_state

    def undo(self):
        GripEditor.apply_state(
            self.owner,
            self.before_state,
        )

    def redo(self):
        GripEditor.apply_state(
            self.owner,
            self.after_state,
        )