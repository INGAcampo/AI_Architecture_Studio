from engines.geometry.line import Line
from engines.geometry.point import Point
from engines.selection.grip_manager import GripManager
from models.cad_circle import CadCircle
from models.cad_line import CadLine
from models.cad_polyline import CadPolyline


def test_line_builds_three_grips():
    line = CadLine(
        Line(
            Point(0, 0, 0),
            Point(10, 0, 0),
        )
    )

    manager = GripManager()
    grips = manager.rebuild_from_selection([line])

    assert len(grips) == 3
    assert grips[1].grip_type == "midpoint"
    assert grips[1].point.x == 5.0


def test_polyline_builds_vertex_grips():
    polyline = CadPolyline()
    polyline.add_point(Point(0, 0, 0))
    polyline.add_point(Point(2, 0, 0))
    polyline.add_point(Point(2, 3, 0))

    manager = GripManager()
    grips = manager.rebuild_from_selection([polyline])

    assert len(grips) == 3
    assert all(
        grip.grip_type == "vertex"
        for grip in grips
    )


def test_circle_builds_five_grips():
    circle = CadCircle(
        center=Point(2, 3, 0),
        radius=4,
    )

    manager = GripManager()
    grips = manager.rebuild_from_selection([circle])

    assert len(grips) == 5
    assert grips[0].grip_type == "center"
    assert grips[1].point.x == 6.0


def test_pick_returns_nearest_grip():
    line = CadLine(
        Line(
            Point(0, 0, 0),
            Point(10, 0, 0),
        )
    )

    manager = GripManager()
    manager.rebuild_from_selection([line])

    picked = manager.pick(
        Point(0.05, 0, 0),
        tolerance=0.2,
    )

    assert picked is not None
    assert picked.index == 0