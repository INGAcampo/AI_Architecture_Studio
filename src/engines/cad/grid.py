"""
AI Architecture Studio
CAD Engine - Grid

Versión: Alpha 0.6
"""

from PySide6.QtGui import QPen, QColor


class Grid:
    def __init__(self):
        self.spacing = 25
        self.major_every = 5

    def draw(self, painter, width, height, camera):
        zoomed_spacing = self.spacing * camera.zoom

        if zoomed_spacing < 5:
            zoomed_spacing = 5

        minor_pen = QPen(QColor(55, 55, 55))
        major_pen = QPen(QColor(85, 85, 85))

        start_x = camera.offset_x % zoomed_spacing
        start_y = camera.offset_y % zoomed_spacing

        x = start_x
        index = 0

        while x <= width:
            painter.setPen(major_pen if index % self.major_every == 0 else minor_pen)
            painter.drawLine(int(x), 0, int(x), height)
            x += zoomed_spacing
            index += 1

        y = start_y
        index = 0

        while y <= height:
            painter.setPen(major_pen if index % self.major_every == 0 else minor_pen)
            painter.drawLine(0, int(y), width, int(y))
            y += zoomed_spacing
            index += 1