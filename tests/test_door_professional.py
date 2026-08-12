"""Pruebas geométricas para DOOR Professional 5.0.5.2."""

from engines.architectural.door_engine import DoorEngine
from engines.geometry.point import Point
from models.architectural.door import Door
from models.architectural.wall import Wall


def test_create_door():
    wall = Wall(
        [
            Point(0.0, 0.0, 0.0),
            Point(10.0, 0.0, 0.0),
        ],
        thickness=0.20,
    )

    door = DoorEngine.create_door(
        wall,
        Point(5.0, 0.0, 0.0),
        width=0.90,
        height=2.10,
    )
    DoorEngine.add_to_wall(wall, door)

    assert wall.door_count == 1
    assert wall.opening_count == 1
    assert door.opening.host_wall is wall
    assert door.opening.door is door
    assert door.opening.opening_type == "Door"


def test_door_plan_geometry():
    wall = Wall(
        [
            Point(0.0, 0.0, 0.0),
            Point(10.0, 0.0, 0.0),
        ],
        thickness=0.20,
    )

    door = DoorEngine.create_door(
        wall,
        Point(5.0, 0.0, 0.0),
    )

    assert len(
        DoorEngine.frame_lines(door)
    ) == 2

    assert DoorEngine.leaf_line(
        door
    ) is not None

    assert len(
        DoorEngine.swing_arc_points(door)
    ) >= 12


def test_door_follows_wnode_edit():
    wall = Wall(
        [
            Point(0.0, 0.0, 0.0),
            Point(10.0, 0.0, 0.0),
        ],
        thickness=0.20,
    )

    door = DoorEngine.create_door(
        wall,
        Point(5.0, 0.0, 0.0),
    )
    DoorEngine.add_to_wall(
        wall,
        door,
    )

    wall.set_path(
        [
            Point(0.0, 0.0, 0.0),
            Point(20.0, 0.0, 0.0),
        ]
    )

    assert abs(
        door.center_point.x - 10.0
    ) < 1.0e-9


def test_flip_options():
    wall = Wall(
        [
            Point(0.0, 0.0, 0.0),
            Point(10.0, 0.0, 0.0),
        ]
    )

    door = DoorEngine.create_door(
        wall,
        Point(5.0, 0.0, 0.0),
    )

    assert door.handedness == Door.LEFT
    door.flip_handedness()
    assert door.handedness == Door.RIGHT

    assert (
        door.swing_direction
        == Door.INWARD
    )
    door.flip_swing_direction()
    assert (
        door.swing_direction
        == Door.OUTWARD
    )
