import pytest

from engines.cad.dynamic_input import (
    DynamicInputManager,
)
from engines.geometry.point import Point


def test_dynamic_input_distance_and_angle():
    manager = DynamicInputManager()

    manager.set_base_point(
        Point(0, 0, 0)
    )

    manager.update_point(
        Point(3, 4, 0)
    )

    assert manager.distance == pytest.approx(
        5.0
    )

    assert manager.angle_degrees == pytest.approx(
        53.130102,
        rel=1e-5,
    )


def test_dynamic_input_horizontal_angle():
    manager = DynamicInputManager()

    manager.set_base_point(
        Point(2, 3, 0)
    )

    manager.update_point(
        Point(12, 3, 0)
    )

    assert manager.distance == pytest.approx(
        10.0
    )

    assert manager.angle_degrees == pytest.approx(
        0.0
    )


def test_dynamic_input_vertical_angle():
    manager = DynamicInputManager()

    manager.set_base_point(
        Point(0, 0, 0)
    )

    manager.update_point(
        Point(0, 8, 0)
    )

    assert manager.distance == pytest.approx(
        8.0
    )

    assert manager.angle_degrees == pytest.approx(
        90.0
    )


def test_toggle_mode():
    manager = DynamicInputManager()

    assert (
        manager.active_mode
        == manager.MODE_DISTANCE
    )

    manager.toggle_mode()

    assert (
        manager.active_mode
        == manager.MODE_ANGLE
    )


def test_toggle_disables_visibility():
    manager = DynamicInputManager()

    manager.set_base_point(
        Point(0, 0, 0)
    )

    assert manager.visible is True

    manager.toggle()

    assert manager.enabled is False
    assert manager.visible is False