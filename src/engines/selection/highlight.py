"""
AI Architecture Studio
Highlight

Foundation 2.8
"""


class Highlight:

    def __init__(self):
        self.element = None

    def set(self, element):
        self.element = element

    def clear(self):
        self.element = None

    def current(self):
        return self.element

    def has_element(self):
        return self.element is not None