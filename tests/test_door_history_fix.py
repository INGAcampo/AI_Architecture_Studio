"""Tests para DOOR History Fix 5.0.5.2.1."""

from core.history.add_door_action import AddDoorAction
from engines.architectural.door_engine import DoorEngine
from engines.geometry.point import Point
from models.architectural.wall import Wall


class SceneStub:
    def __init__(self):
        self.wall_network_signature = "valid"


def make_wall_and_door():
    wall = Wall(
        [
            Point(0.0, 0.0, 0.0),
            Point(20.0, 0.0, 0.0),
        ],
        thickness=0.20,
    )
    door = DoorEngine.create_door(
        wall,
        Point(10.0, 0.0, 0.0),
    )
    DoorEngine.add_to_wall(
        wall,
        door,
    )
    return wall, door


def test_add_is_idempotent():
    wall, door = make_wall_and_door()

    for _ in range(100):
        result = DoorEngine.add_to_wall(
            wall,
            door,
        )
        assert result.door_id == door.door_id

    assert wall.opening_count == 1
    assert wall.door_count == 1
    assert len(wall.openings) == 1


def test_remove_is_idempotent():
    wall, door = make_wall_and_door()

    assert DoorEngine.remove_from_wall(
        wall,
        door,
    )
    assert not DoorEngine.remove_from_wall(
        wall,
        door,
    )

    assert wall.opening_count == 0
    assert wall.door_count == 0


def test_history_stress_undo_redo():
    wall, door = make_wall_and_door()
    scene = SceneStub()
    action = AddDoorAction(
        scene,
        wall,
        door,
    )

    for _ in range(100):
        assert action.undo()
        assert wall.opening_count == 0
        assert wall.door_count == 0

        # Repetir UNDO no altera el estado.
        assert not action.undo()
        assert wall.opening_count == 0

        assert action.redo()
        assert wall.opening_count == 1
        assert wall.door_count == 1

        # Repetir REDO no duplica.
        assert not action.redo()
        assert wall.opening_count == 1
        assert wall.door_count == 1
        assert len(wall.openings) == 1


def test_same_id_cannot_duplicate():
    wall, door = make_wall_and_door()
    cloned_opening = door.opening.clone(
        host_wall=wall,
        preserve_id=True,
    )
    cloned_door = cloned_opening.door

    result = DoorEngine.add_to_wall(
        wall,
        cloned_door,
    )

    assert result.door_id == door.door_id
    assert len(wall.openings) == 1
    assert wall.door_count == 1


def test_clone_new_wall_gets_new_ids():
    wall, door = make_wall_and_door()
    cloned_wall = wall.clone()

    assert cloned_wall.opening_count == 1
    assert cloned_wall.door_count == 1

    cloned_door = cloned_wall.openings[0].door

    assert (
        cloned_door.door_id
        != door.door_id
    )
    assert (
        cloned_wall.openings[0].opening_id
        != door.opening.opening_id
    )
