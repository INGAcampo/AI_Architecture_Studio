"""
AI Architecture Studio
Selection Manager

Professional Selection v1
"""

from engines.selection.selection_set import SelectionSet


class SelectionManager:

    def __init__(self):
        self.selection = SelectionSet()

    def select(self, element):
        self.selection.replace([element])

    def add_to_selection(self, element):
        self.selection.add(element)

    def add_many_to_selection(self, elements):
        self.selection.add_many(elements)

    def replace_selection(self, elements):
        self.selection.replace(elements)

    def remove_from_selection(self, element):
        self.selection.remove(element)

    def toggle_selection(self, element):
        return self.selection.toggle(element)

    def clear(self):
        self.selection.clear()

    def is_selected(self, element):
        return self.selection.contains(element)

    def selected_count(self):
        return self.selection.count()

    def selected_elements(self):
        return self.selection.all()

    def first_selected(self):
        return self.selection.first()

    def last_selected(self):
        return self.selection.last()

    def has_selection(self):
        return not self.selection.is_empty()