"""
AI Architecture Studio
Selection Set

Professional Selection v1
"""


class SelectionSet:

    def __init__(self):
        self._elements = []

    def add(self, element):
        if element is None:
            return False

        if element in self._elements:
            return False

        self._elements.append(element)
        return True

    def add_many(self, elements):
        changed = False

        for element in elements:
            if self.add(element):
                changed = True

        return changed

    def remove(self, element):
        if element not in self._elements:
            return False

        self._elements.remove(element)
        return True

    def toggle(self, element):
        if element in self._elements:
            self._elements.remove(element)
            return False

        self._elements.append(element)
        return True

    def replace(self, elements):
        self.clear()
        self.add_many(elements)

    def clear(self):
        self._elements.clear()

    def contains(self, element):
        return element in self._elements

    def count(self):
        return len(self._elements)

    def all(self):
        return self._elements.copy()

    def first(self):
        if self._elements:
            return self._elements[0]

        return None

    def last(self):
        if self._elements:
            return self._elements[-1]

        return None

    def is_empty(self):
        return not self._elements