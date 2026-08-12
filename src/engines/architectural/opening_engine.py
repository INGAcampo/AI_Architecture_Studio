"""AI Architecture Studio
Architectural Core 5.0.5.2.1 — WALL OPENINGS Engine.
"""

import math

from engines.geometry.point import Point
from models.architectural.opening import WallOpening


class OpeningEngine:
    DEFAULT_WIDTH = 0.90
    DEFAULT_HEIGHT = 2.10
    DEFAULT_SILL_HEIGHT = 0.0
    EPSILON = 1.0e-9

    @staticmethod
    def _parameter_on_segment(point, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        denominator = dx * dx + dy * dy
        if denominator <= OpeningEngine.EPSILON:
            return 0.0
        return (
            (point.x - a.x) * dx
            + (point.y - a.y) * dy
        ) / denominator

    @staticmethod
    def _project(point, a, b):
        t = OpeningEngine._parameter_on_segment(point, a, b)
        t = min(1.0, max(0.0, t))
        return (
            Point(
                a.x + (b.x - a.x) * t,
                a.y + (b.y - a.y) * t,
                getattr(a, "z", 0.0),
            ),
            t,
        )

    @staticmethod
    def distance_to_segment(point, a, b):
        projected, _ = OpeningEngine._project(point, a, b)
        return math.hypot(
            point.x - projected.x,
            point.y - projected.y,
        )

    @classmethod
    def nearest_segment(cls, wall, point):
        path = list(getattr(wall, "path", []) or [])
        best = None
        for index in range(len(path) - 1):
            a = path[index]
            b = path[index + 1]
            projected, parameter = cls._project(point, a, b)
            distance = math.hypot(
                point.x - projected.x,
                point.y - projected.y,
            )
            candidate = {
                "segment_index": index,
                "parameter": parameter,
                "point": projected,
                "distance": distance,
            }
            if best is None or distance < best["distance"]:
                best = candidate
        return best

    @classmethod
    def nearest_wall(cls, walls, point, tolerance=0.75):
        best = None
        for wall in walls or []:
            if wall.__class__.__name__ != "Wall":
                continue
            segment = cls.nearest_segment(wall, point)
            if segment is None:
                continue
            if best is None or segment["distance"] < best["distance"]:
                best = dict(segment)
                best["wall"] = wall
        if best is None or best["distance"] > tolerance:
            return None
        return best

    @staticmethod
    def _segment_length(wall, segment_index):
        path = list(getattr(wall, "path", []) or [])
        if len(path) < 2:
            return 0.0
        index = min(max(0, int(segment_index)), len(path) - 2)
        return path[index].distance_to(path[index + 1])

    @classmethod
    def clamp_opening_to_segment(cls, opening, edge_clearance=1.0e-4):
        wall = opening.host_wall
        length = cls._segment_length(wall, opening.segment_index)
        if length <= cls.EPSILON:
            opening.parameter = 0.5
            return opening

        half_parameter = (opening.width * 0.5) / length
        lower = min(0.5, half_parameter + edge_clearance / length)
        upper = max(0.5, 1.0 - half_parameter - edge_clearance / length)

        if opening.width >= length:
            opening.width = max(cls.EPSILON, length - 2.0 * edge_clearance)
            opening.parameter = 0.5
        else:
            opening.parameter = min(upper, max(lower, opening.parameter))
        return opening

    @classmethod
    def create_opening(
        cls,
        wall,
        point,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        sill_height=DEFAULT_SILL_HEIGHT,
        opening_type=WallOpening.GENERIC,
        name="Hueco",
    ):
        if wall is None or wall.__class__.__name__ != "Wall":
            raise ValueError("El hueco requiere un muro anfitrión.")

        location = cls.nearest_segment(wall, point)
        if location is None:
            raise ValueError("El muro no tiene segmentos válidos.")

        opening = WallOpening(
            host_wall=wall,
            segment_index=location["segment_index"],
            parameter=location["parameter"],
            width=width,
            height=height,
            sill_height=sill_height,
            opening_type=opening_type,
            name=name,
        )
        cls.clamp_opening_to_segment(opening)
        return opening

    @staticmethod
    def _opening_id(opening):
        return getattr(
            opening,
            "opening_id",
            None,
        )

    @classmethod
    def find_opening(
        cls,
        wall,
        opening=None,
        opening_id=None,
    ):
        target_id = (
            opening_id
            or cls._opening_id(opening)
        )

        for candidate in list(
            getattr(wall, "openings", []) or []
        ):
            if candidate is opening:
                return candidate

            if (
                target_id is not None
                and cls._opening_id(candidate)
                == target_id
            ):
                return candidate

        return None

    @classmethod
    def normalize_wall_openings(cls, wall):
        unique = []
        seen_ids = set()
        seen_objects = set()

        for opening in list(
            getattr(wall, "openings", []) or []
        ):
            object_key = id(opening)
            opening_id = cls._opening_id(opening)

            if object_key in seen_objects:
                continue

            if (
                opening_id is not None
                and opening_id in seen_ids
            ):
                continue

            opening.host_wall = wall
            unique.append(opening)
            seen_objects.add(object_key)

            if opening_id is not None:
                seen_ids.add(opening_id)

        wall.openings = unique
        return unique

    @classmethod
    def add_to_wall(cls, wall, opening):
        if wall is None:
            raise ValueError(
                "El hueco requiere un muro anfitrión."
            )

        if getattr(wall, "openings", None) is None:
            wall.openings = []

        cls.normalize_wall_openings(wall)

        existing = cls.find_opening(
            wall,
            opening=opening,
        )

        if existing is None:
            opening.host_wall = wall
            wall.openings.append(opening)
            result = opening
        else:
            existing.host_wall = wall
            result = existing

        updater = getattr(
            wall,
            "_update_properties",
            None,
        )
        if callable(updater):
            updater()

        return result

    @classmethod
    def remove_from_wall(cls, wall, opening):
        if wall is None:
            return False

        openings = getattr(
            wall,
            "openings",
            None,
        )
        if openings is None:
            return False

        target = cls.find_opening(
            wall,
            opening=opening,
        )

        if target is None:
            return False

        wall.openings = [
            candidate
            for candidate in openings
            if (
                candidate is not target
                and cls._opening_id(candidate)
                != cls._opening_id(target)
            )
        ]

        updater = getattr(
            wall,
            "_update_properties",
            None,
        )
        if callable(updater):
            updater()

        return True

    @classmethod
    def cutter_polygon(cls, opening, wall_depth_factor=2.50):
        """Rectángulo mundial usado para sustraer el hueco en planta."""
        wall = opening.host_wall
        path = list(getattr(wall, "path", []) or [])
        if len(path) < 2:
            return []

        index = min(opening.segment_index, len(path) - 2)
        a = path[index]
        b = path[index + 1]
        dx = b.x - a.x
        dy = b.y - a.y
        length = math.hypot(dx, dy)
        if length <= cls.EPSILON:
            return []

        ux = dx / length
        uy = dy / length
        nx = -uy
        ny = ux

        center = opening.center_point
        half_width = opening.width * 0.5
        half_depth = (
            max(float(getattr(wall, "thickness", 0.20)), 0.01)
            * wall_depth_factor
        )

        return [
            Point(
                center.x - ux * half_width - nx * half_depth,
                center.y - uy * half_width - ny * half_depth,
                center.z,
            ),
            Point(
                center.x + ux * half_width - nx * half_depth,
                center.y + uy * half_width - ny * half_depth,
                center.z,
            ),
            Point(
                center.x + ux * half_width + nx * half_depth,
                center.y + uy * half_width + ny * half_depth,
                center.z,
            ),
            Point(
                center.x - ux * half_width + nx * half_depth,
                center.y - uy * half_width + ny * half_depth,
                center.z,
            ),
        ]

    @classmethod
    def jamb_lines(cls, opening):
        """Devuelve dos líneas transversales para representar las jambas."""
        wall = opening.host_wall
        path = list(getattr(wall, "path", []) or [])
        if len(path) < 2:
            return []

        index = min(opening.segment_index, len(path) - 2)
        a = path[index]
        b = path[index + 1]
        dx = b.x - a.x
        dy = b.y - a.y
        length = math.hypot(dx, dy)
        if length <= cls.EPSILON:
            return []

        ux = dx / length
        uy = dy / length
        nx = -uy
        ny = ux
        center = opening.center_point
        half_width = opening.width * 0.5
        half_depth = max(float(getattr(wall, "thickness", 0.20)), 0.01)

        result = []
        for sign in (-1.0, 1.0):
            cx = center.x + ux * half_width * sign
            cy = center.y + uy * half_width * sign
            result.append(
                (
                    Point(cx - nx * half_depth, cy - ny * half_depth, center.z),
                    Point(cx + nx * half_depth, cy + ny * half_depth, center.z),
                )
            )
        return result

    @classmethod
    def update_after_wall_change(cls, wall):
        """Mantiene cada hueco dentro de su segmento tras editar el muro."""
        path = list(getattr(wall, "path", []) or [])
        if len(path) < 2:
            return
        for opening in list(getattr(wall, "openings", []) or []):
            opening.host_wall = wall
            opening.segment_index = min(
                max(0, opening.segment_index),
                len(path) - 2,
            )
            cls.clamp_opening_to_segment(opening)
