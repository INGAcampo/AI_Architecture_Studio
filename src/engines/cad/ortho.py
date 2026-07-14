"""
AI Architecture Studio
CAD Engine - ORTHO Manager

Foundation 4.3
"""

from engines.geometry.point import Point


class OrthoManager:

    def __init__(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled

        print(
            f"ORTHO "
            f"{'ACTIVADO' if self.enabled else 'DESACTIVADO'}"
        )

        return self.enabled

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

    def apply(self, base_point, current_point):
        if not self.enabled:
            return current_point

        if base_point is None or current_point is None:
            return current_point

        dx = current_point.x - base_point.x
        dy = current_point.y - base_point.y

        if abs(dx) >= abs(dy):
            return Point(
                current_point.x,
                base_point.y,
                current_point.z,
            )

        return Point(
            base_point.x,
            current_point.y,
            current_point.z,
        )