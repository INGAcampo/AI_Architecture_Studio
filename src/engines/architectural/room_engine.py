"""ROOM Engine 5.0.7.3."""

import math

from engines.architectural.room_detector import RoomDetector
from engines.geometry.point import Point
from models.architectural.room import Room


class RoomEngine:
    EPSILON = 1.0e-8

    @staticmethod
    def compute_area(points):
        if len(points) < 3:
            return 0.0
        return abs(
            0.5
            * sum(
                points[index].x * points[(index + 1) % len(points)].y
                - points[(index + 1) % len(points)].x * points[index].y
                for index in range(len(points))
            )
        )

    @staticmethod
    def compute_perimeter(points):
        if len(points) < 2:
            return 0.0
        return sum(
            math.hypot(
                points[(index + 1) % len(points)].x - points[index].x,
                points[(index + 1) % len(points)].y - points[index].y,
            )
            for index in range(len(points))
        )

    @staticmethod
    def boundary_key(points, precision=6):
        coordinates = [
            (round(point.x, precision), round(point.y, precision))
            for point in points
        ]
        if not coordinates:
            return tuple()

        variants = []
        for candidate in (coordinates, list(reversed(coordinates))):
            for offset in range(len(candidate)):
                variants.append(
                    tuple(candidate[offset:] + candidate[:offset])
                )
        return min(variants)

    @classmethod
    def detect_rooms(cls, scene):
        return RoomDetector.detect(scene)

    @classmethod
    def detect_at_point(cls, scene, point):
        return RoomDetector.detect_at_point(scene, point)

    @classmethod
    def create_room(cls, scene, point, name=None):
        boundary = cls.detect_at_point(scene, point)
        if boundary is None:
            return None

        room = Room(
            boundary=boundary,
            name=name or cls.next_name(scene),
            seed_point=point,
        )
        return room

    @staticmethod
    def scene_rooms(scene):
        if scene is None:
            return []
        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        return [
            element for element in elements
            if element.__class__.__name__ == "Room"
        ]

    @classmethod
    def next_name(cls, scene):
        return f"Ambiente {len(cls.scene_rooms(scene)) + 1}"

    @classmethod
    def equivalent_room(cls, scene, boundary_key):
        for room in cls.scene_rooms(scene):
            if getattr(room, "boundary_key", None) == boundary_key:
                return room
        return None

    @classmethod
    def add_to_scene(cls, scene, room):
        if scene is None or room is None:
            return False

        existing = cls.equivalent_room(scene, room.boundary_key)
        if existing is not None:
            return existing

        adder = getattr(scene, "add_element", None)
        if callable(adder):
            adder(room)
            cls.invalidate_scene(scene)
            return room
        return False

    @classmethod
    def remove_from_scene(cls, scene, room):
        if scene is None or room is None:
            return False

        remover = getattr(scene, "remove_element", None)
        if callable(remover):
            remover(room)
            cls.invalidate_scene(scene)
            return True

        elements = getattr(scene, "elements", None)
        if isinstance(elements, list) and room in elements:
            elements.remove(room)
            cls.invalidate_scene(scene)
            return True
        return False

    @staticmethod
    def invalidate_scene(scene):
        if scene is not None:
            scene.room_geometry_signature = None

    @classmethod
    def update_scene_rooms(cls, scene):
        if scene is None:
            return []

        rooms = cls.scene_rooms(scene)
        if not rooms:
            return rooms

        wall_signature = getattr(scene, "wall_network_signature", None)
        if getattr(scene, "room_geometry_signature", None) == wall_signature:
            return rooms

        for room in rooms:
            seed = getattr(room, "seed_point", None)
            if seed is None:
                room.invalidate()
                continue

            boundary = cls.detect_at_point(scene, seed)
            if boundary is None:
                room.invalidate()
                continue

            room.update_geometry(
                boundary,
                boundary_key=cls.boundary_key(boundary),
            )

        scene.room_geometry_signature = wall_signature
        return rooms
