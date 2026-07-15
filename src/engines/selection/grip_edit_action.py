"""
AI Architecture Studio
History Action - Grip Edit

Professional Grips v1 - Package 4A
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

    def execute(self):
        return GripEditor.apply_state(
            self.owner,
            self.after_state,
        )

    def undo(self):
        return GripEditor.apply_state(
            self.owner,
            self.before_state,
        )

    def redo(self):
        return GripEditor.apply_state(
            self.owner,
            self.after_state,
        )