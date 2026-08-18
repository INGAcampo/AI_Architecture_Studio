"""
AI Architecture Studio
Grip Manager

Professional Grips v1
"""

from engines.geometry.point import Point
from engines.selection.grip import Grip


class GripManager:

    TYPE_ENDPOINT = "endpoint"
    TYPE_MIDPOINT = "midpoint"
    TYPE_CENTER = "center"
    TYPE_VERTEX = "vertex"

    def __init__(self):
        self._grips = []
        self._active_grip = None
        self._hovered_grip = None

    def clear(self):
        self._grips.clear()
        self._active_grip = None
        self._hovered_grip = None

    def all_grips(self):
        return list(self._grips)

    def active_grip(self):
        return self._active_grip

    def hovered_grip(self):
        return self._hovered_grip

    def rebuild_from_selection(self, elements):
        self.clear()

        for element in elements:
            self._grips.extend(
                self._build_element_grips(
                    element
                )
            )

        return self.all_grips()

    def _build_element_grips(self, element):
        element_type = (
            element.__class__.__name__
        )

        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__
            == "Line"
        ):
            midpoint = Point(
                (geometry.start.x + geometry.end.x) / 2.0,
                (geometry.start.y + geometry.end.y) / 2.0,
                (geometry.start.z + geometry.end.z) / 2.0,
            )

            return [
                Grip(
                    owner=element,
                    point=self._copy_point(geometry.start),
                    grip_type=self.TYPE_ENDPOINT,
                    index=0,
                ),
                Grip(
                    owner=element,
                    point=midpoint,
                    grip_type=self.TYPE_MIDPOINT,
                ),
                Grip(
                    owner=element,
                    point=self._copy_point(geometry.end),
                    grip_type=self.TYPE_ENDPOINT,
                    index=1,
                ),
            ]

        if element_type == "CadPolyline":
            return self._build_vertex_grips(
                element,
                element.points,
            )

        if element_type == "CadRectangle":
            return self._build_vertex_grips(
                element,
                element.polyline.points,
            )

        if element_type == "CadCircle":
            center = element.center
            radius = element.radius

            return [
                Grip(
                    owner=element,
                    point=self._copy_point(center),
                    grip_type=self.TYPE_CENTER,
                    index=0,
                ),
                Grip(
                    owner=element,
                    point=Point(
                        center.x + radius,
                        center.y,
                        center.z,
                    ),
                    grip_type=self.TYPE_ENDPOINT,
                    index=1,
                ),
                Grip(
                    owner=element,
                    point=Point(
                        center.x,
                        center.y + radius,
                        center.z,
                    ),
                    grip_type=self.TYPE_ENDPOINT,
                    index=2,
                ),
                Grip(
                    owner=element,
                    point=Point(
                        center.x - radius,
                        center.y,
                        center.z,
                    ),
                    grip_type=self.TYPE_ENDPOINT,
                    index=3,
                ),
                Grip(
                    owner=element,
                    point=Point(
                        center.x,
                        center.y - radius,
                        center.z,
                    ),
                    grip_type=self.TYPE_ENDPOINT,
                    index=4,
                ),
            ]

        return []

    def _build_vertex_grips(
        self,
        element,
        points,
    ):
        return [
            Grip(
                owner=element,
                point=self._copy_point(point),
                grip_type=self.TYPE_VERTEX,
                index=index,
            )
            for index, point in enumerate(points)
        ]

    def pick(
        self,
        point,
        tolerance=0.18,
    ):
        nearest = None
        nearest_distance = None

        for grip in self._grips:
            distance = point.distance_to(
                grip.point
            )

            if distance > tolerance:
                continue

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest = grip
                nearest_distance = distance

        return nearest

    def set_hovered(self, grip):
        if (
            self._hovered_grip is not None
            and self._hovered_grip is not grip
        ):
            self._hovered_grip.set_hovered(False)

        self._hovered_grip = grip

        if grip is not None:
            grip.set_hovered(True)

    def activate(self, grip):
        if self._active_grip is not None:
            self._active_grip.deactivate()

        self._active_grip = grip

        if grip is not None:
            grip.activate()

    def deactivate(self):
        if self._active_grip is not None:
            self._active_grip.deactivate()

        self._active_grip = None

    @staticmethod
    def _copy_point(point):
        return Point(
            point.x,
            point.y,
            point.z,
        )