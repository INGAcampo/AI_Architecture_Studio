"""Detección de recintos cerrados sobre WALL NETWORK."""

from engines.architectural.room_graph import RoomGraph


class RoomDetector:
    EPSILON = 1.0e-8

    @staticmethod
    def point_in_polygon(point, polygon):
        if len(polygon) < 3:
            return False

        inside = False
        x, y = point.x, point.y
        previous = polygon[-1]

        for current in polygon:
            x1, y1 = previous.x, previous.y
            x2, y2 = current.x, current.y

            denominator = y2 - y1
            intersects = (
                (y1 > y) != (y2 > y)
                and x
                < (x2 - x1) * (y - y1)
                / (denominator if abs(denominator) > 1.0e-12 else 1.0e-12)
                + x1
            )
            if intersects:
                inside = not inside
            previous = current

        return inside

    @classmethod
    def detect(cls, scene):
        graph = RoomGraph.from_scene(scene)
        return graph.faces()

    @classmethod
    def detect_at_point(cls, scene, point):
        candidates = [
            polygon
            for polygon in cls.detect(scene)
            if cls.point_in_polygon(point, polygon)
        ]
        if not candidates:
            return None

        return min(
            candidates,
            key=lambda polygon: abs(RoomGraph.signed_area(polygon)),
        )
