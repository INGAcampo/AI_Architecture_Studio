from engines.geometry.line import Line
from engines.geometry.point import Point
from engines.selection.grip_editor import GripEditor
from engines.selection.grip_manager import GripManager
from models.cad_line import CadLine
from models.cad_polyline import CadPolyline
from models.cad_rectangle import CadRectangle


def build_line():
    return CadLine(
        Line(
            Point(0, 0, 0),
            Point(10, 0, 0),
        )
    )


def build_polyline():
    polyline = CadPolyline()
    polyline.add_point(
        Point(0, 0, 0)
    )
    polyline.add_point(
        Point(4, 0, 0)
    )
    polyline.add_point(
        Point(4, 3, 0)
    )
    return polyline


def build_rectangle():
    polyline = CadPolyline()
    polyline.add_point(
        Point(0, 0, 0)
    )
    polyline.add_point(
        Point(6, 0, 0)
    )
    polyline.add_point(
        Point(6, 4, 0)
    )
    polyline.add_point(
        Point(0, 4, 0)
    )
    polyline.close()

    return CadRectangle(
        polyline
    )


def test_line_endpoint_edit_still_works():
    line = build_line()
    grips = (
        GripManager()
        .rebuild_from_selection(
            [line]
        )
    )

    editor = GripEditor()

    assert editor.begin(
        grips[0]
    )

    assert editor.update(
        Point(2, 1, 0)
    )

    editor.finish()

    assert line.geometry.start.x == 2
    assert line.geometry.start.y == 1


def test_polyline_vertex_edit():
    polyline = build_polyline()

    grips = (
        GripManager()
        .rebuild_from_selection(
            [polyline]
        )
    )

    editor = GripEditor()

    assert editor.begin(
        grips[1]
    )

    assert editor.update(
        Point(7, 2, 0)
    )

    result = editor.finish()

    assert polyline.points[1].x == 7
    assert polyline.points[1].y == 2
    assert result["before"]["points"][1].x == 4
    assert result["after"]["points"][1].x == 7


def test_polyline_cancel_restores_vertex():
    polyline = build_polyline()

    grips = (
        GripManager()
        .rebuild_from_selection(
            [polyline]
        )
    )

    editor = GripEditor()

    assert editor.begin(
        grips[0]
    )

    assert editor.update(
        Point(8, 9, 0)
    )

    editor.cancel()

    assert polyline.points[0].x == 0
    assert polyline.points[0].y == 0


def test_rectangle_corner_preserves_rectangle():
    rectangle = build_rectangle()

    grips = (
        GripManager()
        .rebuild_from_selection(
            [rectangle]
        )
    )

    editor = GripEditor()

    assert editor.begin(
        grips[2]
    )

    assert editor.update(
        Point(8, 6, 0)
    )

    editor.finish()

    points = rectangle.polyline.points

    assert points[2].x == 8
    assert points[2].y == 6

    assert points[1].x == 8
    assert points[1].y == 0

    assert points[3].x == 0
    assert points[3].y == 6

    assert rectangle.polyline.closed is True


def test_rectangle_cancel_restores_shape():
    rectangle = build_rectangle()

    grips = (
        GripManager()
        .rebuild_from_selection(
            [rectangle]
        )
    )

    editor = GripEditor()

    assert editor.begin(
        grips[0]
    )

    assert editor.update(
        Point(-3, -2, 0)
    )

    editor.cancel()

    points = rectangle.polyline.points

    assert points[0].x == 0
    assert points[0].y == 0
    assert points[1].x == 6
    assert points[3].y == 4