"""
AI Architecture Studio
Selection Set

Foundation 2.8
"""


class SelectionSet:

    def __init__(self):
        self._elements = []

    def add(self, element):

        if element not in self._elements:
            self._elements.append(element)

    def remove(self, element):

        if element in self._elements:
            self._elements.remove(element)

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