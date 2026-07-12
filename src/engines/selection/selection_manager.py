"""
AI Architecture Studio
Selection Manager

Foundation 2.8
"""

from engines.selection.selection_set import SelectionSet


class SelectionManager:

    def __init__(self):
        self.selection = SelectionSet()

    def select(self, element):
        self.selection.clear()
        self.selection.add(element)

    def add_to_selection(self, element):
        self.selection.add(element)

    def clear(self):
        self.selection.clear()

    def selected_count(self):
        return self.selection.count()

    def selected_elements(self):
        return self.selection.all()

    def first_selected(self):
        return self.selection.first()