"""Pruebas de Architectural Core 5.0.5.1 — WALL OPENINGS."""

from engines.architectural.opening_engine import OpeningEngine
from engines.geometry.point import Point
from models.architectural.wall import Wall


def test_create_opening_on_wall():
    wall = Wall(
        [Point(0.0, 0.0, 0.0), Point(10.0, 0.0, 0.0)],
        thickness=0.20,
    )
    opening = OpeningEngine.create_opening(
        wall,
        Point(5.0, 0.2, 0.0),
        width=1.20,
        height=2.10,
    )
    OpeningEngine.add_to_wall(wall, opening)

    assert wall.opening_count == 1
    assert opening.segment_index == 0
    assert abs(opening.parameter - 0.5) < 1.0e-9
    assert abs(opening.center_point.x - 5.0) < 1.0e-9
    assert len(OpeningEngine.cutter_polygon(opening)) == 4


def test_opening_follows_wall_node_edit():
    wall = Wall(
        [Point(0.0, 0.0, 0.0), Point(10.0, 0.0, 0.0)],
        thickness=0.20,
    )
    opening = OpeningEngine.create_opening(
        wall,
        Point(5.0, 0.0, 0.0),
        width=1.0,
    )
    OpeningEngine.add_to_wall(wall, opening)

    wall.set_path(
        [Point(0.0, 0.0, 0.0), Point(20.0, 0.0, 0.0)]
    )
    assert abs(opening.center_point.x - 10.0) < 1.0e-9


def test_opening_is_clamped_inside_short_segment():
    wall = Wall(
        [Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0)],
        thickness=0.20,
    )
    opening = OpeningEngine.create_opening(
        wall,
        Point(0.95, 0.0, 0.0),
        width=0.80,
    )
    assert 0.0 < opening.parameter < 1.0
