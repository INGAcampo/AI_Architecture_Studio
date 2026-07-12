"""
AI Architecture Studio
History Manager

Foundation 3.2
"""


class HistoryManager:

    def __init__(self):

        self.undo_stack = []
        self.redo_stack = []

    def push(self, action):

        self.undo_stack.append(action)

        self.redo_stack.clear()

    def undo(self):

        if not self.undo_stack:
            return

        action = self.undo_stack.pop()

        action.undo()

        self.redo_stack.append(action)

    def redo(self):

        if not self.redo_stack:
            return

        action = self.redo_stack.pop()

        action.redo()

        self.undo_stack.append(action)

    def undo_count(self):

        return len(self.undo_stack)

    def redo_count(self):

        return len(self.redo_stack)