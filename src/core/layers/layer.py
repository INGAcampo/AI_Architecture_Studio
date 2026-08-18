"""
AI Architecture Studio
Layer model
"""


class Layer:
    def __init__(self, name, color="#DADADA", visible=True, locked=False, line_weight=1):
        self.name = name
        self.color = color
        self.visible = visible
        self.locked = locked
        self.line_weight = line_weight

    def to_dict(self):
        return {
            "name": self.name,
            "color": self.color,
            "visible": self.visible,
            "locked": self.locked,
            "line_weight": self.line_weight,
        }
