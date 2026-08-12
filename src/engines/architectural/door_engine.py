"""AI Architecture Studio
Architectural Core 5.0.5.2.1 — DOOR Engine.
"""

import math

from engines.architectural.opening_engine import (
    OpeningEngine,
)
from engines.geometry.point import Point
from models.architectural.door import Door
from models.architectural.opening import WallOpening


class DoorEngine:
    DEFAULT_WIDTH = 0.90
    DEFAULT_HEIGHT = 2.10
    EPSILON = 1.0e-9

    @staticmethod
    def _axes(door):
        opening = door.opening
        wall = opening.host_wall
        path = list(
            getattr(wall, "path", []) or []
        )

        if len(path) < 2:
            return None

        index = min(
            opening.segment_index,
            len(path) - 2,
        )
        first = path[index]
        second = path[index + 1]

        dx = second.x - first.x
        dy = second.y - first.y
        length = math.hypot(dx, dy)

        if length <= DoorEngine.EPSILON:
            return None

        tangent = (
            dx / length,
            dy / length,
        )
        normal = (
            -tangent[1],
            tangent[0],
        )

        return {
            "tangent": tangent,
            "normal": normal,
            "center": opening.center_point,
            "thickness": max(
                float(
                    getattr(
                        wall,
                        "thickness",
                        0.20,
                    )
                ),
                0.01,
            ),
        }

    @classmethod
    def create_door(
        cls,
        wall,
        point,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        handedness=Door.LEFT,
        swing_direction=Door.INWARD,
    ):
        opening = OpeningEngine.create_opening(
            wall,
            point,
            width=width,
            height=height,
            sill_height=0.0,
            opening_type=WallOpening.DOOR,
            name="Hueco de puerta",
        )

        door = Door(
            opening=opening,
            width=opening.width,
            height=height,
            handedness=handedness,
            swing_direction=swing_direction,
        )
        opening.attach_door(door)
        return door

    @staticmethod
    def _door_id(door):
        return getattr(
            door,
            "door_id",
            None,
        )

    @classmethod
    def find_door(
        cls,
        wall,
        door=None,
        door_id=None,
    ):
        target_id = (
            door_id
            or cls._door_id(door)
        )

        for opening in list(
            getattr(wall, "openings", []) or []
        ):
            candidate = getattr(
                opening,
                "door",
                None,
            )

            if candidate is door:
                return candidate

            if (
                candidate is not None
                and target_id is not None
                and cls._door_id(candidate)
                == target_id
            ):
                return candidate

        return None

    @classmethod
    def contains_door(
        cls,
        wall,
        door=None,
        door_id=None,
    ):
        return (
            cls.find_door(
                wall,
                door=door,
                door_id=door_id,
            )
            is not None
        )

    @classmethod
    def add_to_wall(cls, wall, door):
        if wall is None:
            raise ValueError(
                "La puerta requiere un muro anfitrión."
            )
        if door is None:
            raise ValueError(
                "No se puede agregar una puerta vacía."
            )
        if door.opening is None:
            raise ValueError(
                "La puerta requiere un hueco anfitrión."
            )

        existing_door = cls.find_door(
            wall,
            door=door,
        )

        if existing_door is not None:
            existing_opening = existing_door.opening
            existing_opening.attach_door(
                existing_door
            )
            OpeningEngine.add_to_wall(
                wall,
                existing_opening,
            )
            return existing_door

        opening = door.opening
        existing_opening = OpeningEngine.find_opening(
            wall,
            opening=opening,
        )

        if existing_opening is not None:
            current_door = getattr(
                existing_opening,
                "door",
                None,
            )

            if current_door is not None:
                current_id = cls._door_id(
                    current_door
                )
                incoming_id = cls._door_id(
                    door
                )

                if current_id == incoming_id:
                    return current_door

                raise ValueError(
                    "El hueco ya contiene otra puerta."
                )

            existing_opening.attach_door(
                door
            )
            opening = existing_opening
        else:
            opening.attach_door(door)

        OpeningEngine.add_to_wall(
            wall,
            opening,
        )
        return door

    @classmethod
    def remove_from_wall(cls, wall, door):
        if wall is None or door is None:
            return False

        existing = cls.find_door(
            wall,
            door=door,
        )

        if existing is None:
            return False

        opening = existing.opening

        if opening is None:
            return False

        removed = OpeningEngine.remove_from_wall(
            wall,
            opening,
        )

        if removed:
            existing.opening = opening

        return removed

    @classmethod
    def hinge_and_latch(cls, door):
        axes = cls._axes(door)

        if axes is None:
            return None

        ux, uy = axes["tangent"]
        center = axes["center"]
        half_width = door.width * 0.5

        hinge_sign = (
            -1.0
            if door.handedness == Door.LEFT
            else 1.0
        )

        hinge = Point(
            center.x
            + ux * half_width * hinge_sign,
            center.y
            + uy * half_width * hinge_sign,
            center.z,
        )
        latch = Point(
            center.x
            - ux * half_width * hinge_sign,
            center.y
            - uy * half_width * hinge_sign,
            center.z,
        )

        return hinge, latch, axes

    @classmethod
    def frame_lines(cls, door):
        result = cls.hinge_and_latch(door)

        if result is None:
            return []

        hinge, latch, axes = result
        nx, ny = axes["normal"]
        half_depth = axes["thickness"] * 0.70

        lines = []

        for point in (hinge, latch):
            lines.append(
                (
                    Point(
                        point.x - nx * half_depth,
                        point.y - ny * half_depth,
                        point.z,
                    ),
                    Point(
                        point.x + nx * half_depth,
                        point.y + ny * half_depth,
                        point.z,
                    ),
                )
            )

        return lines

    @classmethod
    def leaf_line(cls, door):
        result = cls.hinge_and_latch(door)

        if result is None:
            return None

        hinge, _, axes = result
        ux, uy = axes["tangent"]
        nx, ny = axes["normal"]

        tangent_sign = (
            1.0
            if door.handedness == Door.LEFT
            else -1.0
        )
        normal_sign = (
            1.0
            if door.swing_direction == Door.INWARD
            else -1.0
        )

        open_direction_x = (
            nx * normal_sign
        )
        open_direction_y = (
            ny * normal_sign
        )

        leaf_end = Point(
            hinge.x
            + open_direction_x * door.width,
            hinge.y
            + open_direction_y * door.width,
            hinge.z,
        )

        return hinge, leaf_end

    @classmethod
    def swing_arc_points(
        cls,
        door,
        segments=24,
    ):
        result = cls.hinge_and_latch(door)

        if result is None:
            return []

        hinge, latch, axes = result
        ux, uy = axes["tangent"]
        nx, ny = axes["normal"]

        closed_vector = (
            latch.x - hinge.x,
            latch.y - hinge.y,
        )

        normal_sign = (
            1.0
            if door.swing_direction == Door.INWARD
            else -1.0
        )

        target_vector = (
            nx * normal_sign * door.width,
            ny * normal_sign * door.width,
        )

        start_angle = math.atan2(
            closed_vector[1],
            closed_vector[0],
        )
        end_angle = math.atan2(
            target_vector[1],
            target_vector[0],
        )

        delta = (
            end_angle - start_angle
        )

        while delta <= -math.pi:
            delta += 2.0 * math.pi
        while delta > math.pi:
            delta -= 2.0 * math.pi

        if door.handedness == Door.RIGHT:
            if delta > 0.0:
                delta -= 2.0 * math.pi
            if delta < -math.pi:
                delta += 2.0 * math.pi
        else:
            if delta < 0.0:
                delta += 2.0 * math.pi
            if delta > math.pi:
                delta -= 2.0 * math.pi

        points = []

        for index in range(segments + 1):
            parameter = index / segments
            angle = start_angle + delta * parameter

            points.append(
                Point(
                    hinge.x
                    + math.cos(angle) * door.width,
                    hinge.y
                    + math.sin(angle) * door.width,
                    hinge.z,
                )
            )

        return points

    @classmethod
    def update_after_wall_change(cls, wall):
        OpeningEngine.update_after_wall_change(
            wall
        )

        for opening in list(
            getattr(wall, "openings", []) or []
        ):
            door = getattr(
                opening,
                "door",
                None,
            )

            if door is None:
                continue

            door.opening = opening
            door.width = opening.width
            door.height = opening.height
