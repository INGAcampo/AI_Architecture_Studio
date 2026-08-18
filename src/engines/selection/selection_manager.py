"""
AI Architecture Studio
Selection Manager

Professional Grips v1
"""

from engines.selection.grip_manager import GripManager
from engines.selection.selection_set import SelectionSet


class SelectionManager:

    def __init__(self):
        self.selection = SelectionSet()
        self.grips = GripManager()

    def rebuild_grips(self):
        self.grips.rebuild_from_selection(
            self.selection.all()
        )

    def select(self, element):
        if element is None:
            self.selection.clear()
        else:
            self.selection.replace(
                [element]
            )

        self.rebuild_grips()

    def add_to_selection(self, element):
        self.selection.add(element)
        self.rebuild_grips()

    def add_many_to_selection(self, elements):
        self.selection.add_many(elements)
        self.rebuild_grips()

    def replace_selection(self, elements):
        self.selection.replace(elements)
        self.rebuild_grips()

    def remove_from_selection(self, element):
        self.selection.remove(element)
        self.rebuild_grips()

    def toggle_selection(self, element):
        selected = self.selection.toggle(
            element
        )

        self.rebuild_grips()

        return selected

    def clear(self):
        self.selection.clear()
        self.grips.clear()

    def is_selected(self, element):
        return self.selection.contains(
            element
        )

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

    def all_grips(self):
        return self.grips.all_grips()

    def hovered_grip(self):
        return self.grips.hovered_grip()

    def active_grip(self):
        return self.grips.active_grip()

    def set_hovered_grip(self, grip):
        self.grips.set_hovered(grip)

    def activate_grip(self, grip):
        self.grips.activate(grip)

    def deactivate_grip(self):
        self.grips.deactivate()

    def pick_grip(
        self,
        point,
        tolerance=0.18,
    ):
        return self.grips.pick(
            point,
            tolerance=tolerance,
        )