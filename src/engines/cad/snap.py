"""
AI Architecture Studio
CAD Engine - Object Snap

Versión: Foundation 1.4
"""

from engines.geometry.point import Point


class SnapEngine:
    def __init__(self):
        self.enabled = True
        self.snap_distance = 0.25  # metros

    def snap_point(self, cursor_point, scene):
        if not self.enabled or scene is None:
            return cursor_point, None

        nearest_point = None
        nearest_distance = None
        snap_type = None

        for element in scene.get_elements():
            geometry = getattr(element, "geometry", None)

            if geometry is None:
                continue

            if geometry.__class__.__name__ == "Line":
                candidates = [
                    ("Endpoint", geometry.start),
                    ("Endpoint", geometry.end),
                    ("Midpoint", geometry.midpoint),
                ]

                for candidate_type, candidate_point in candidates:
                    distance = cursor_point.distance_to(candidate_point)

                    if distance <= self.snap_distance:
                        if nearest_distance is None or distance < nearest_distance:
                            nearest_distance = distance
                            nearest_point = candidate_point
                            snap_type = candidate_type

        if nearest_point:
            return Point(nearest_point.x, nearest_point.y, nearest_point.z), snap_type

        return cursor_point, None