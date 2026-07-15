from engines.geometry.line import Line
from engines.geometry.point import Point
from engines.selection.grip_editor import GripEditor
from engines.selection.grip_manager import GripManager
from models.cad_line import CadLine


def build_line():
    return CadLine(
        Line(
            Point(0, 0, 0),
            Point(10, 0, 0),
        )
    )


def test_edit_line_start_endpoint():
    line = build_line()
    grips = GripManager().rebuild_from_selection([line])

    editor = GripEditor()
    assert editor.begin(grips[0])
    assert editor.update(Point(2, 3, 0))

    result = editor.finish()

    assert line.geometry.start.x == 2
    assert line.geometry.start.y == 3
    assert result["before"]["start"].x == 0
    assert result["after"]["start"].x == 2


def test_edit_line_end_endpoint():
    line = build_line()
    grips = GripManager().rebuild_from_selection([line])

    editor = GripEditor()
    assert editor.begin(grips[2])
    assert editor.update(Point(12, 4, 0))
    editor.finish()

    assert line.geometry.end.x == 12
    assert line.geometry.end.y == 4


def test_midpoint_moves_complete_line():
    line = build_line()
    grips = GripManager().rebuild_from_selection([line])

    editor = GripEditor()
    assert editor.begin(grips[1])
    assert editor.update(Point(7, 3, 0))
    editor.finish()

    assert line.geometry.start.x == 2
    assert line.geometry.start.y == 3
    assert line.geometry.end.x == 12
    assert line.geometry.end.y == 3


def test_cancel_restores_original_geometry():
    line = build_line()
    grips = GripManager().rebuild_from_selection([line])

    editor = GripEditor()
    assert editor.begin(grips[0])
    assert editor.update(Point(8, 8, 0))

    editor.cancel()

    assert line.geometry.start.x == 0
    assert line.geometry.start.y == 0