"""
Pruebas para Coordinate Parser Professional.
"""

import math

import pytest

from engines.cad.coordinate_parser import (
    CoordinateParseError,
    CoordinateParser,
)
from engines.geometry.point import Point


def assert_point(point, x, y, tolerance=1e-9):
    assert math.isclose(
        point.x,
        x,
        abs_tol=tolerance,
    )
    assert math.isclose(
        point.y,
        y,
        abs_tol=tolerance,
    )


def test_absolute_cartesian():
    point = CoordinateParser.parse(
        "10,25"
    )
    assert_point(point, 10.0, 25.0)


def test_relative_cartesian():
    point = CoordinateParser.parse(
        "@10,5",
        base_point=Point(2.0, 3.0, 0.0),
    )
    assert_point(point, 12.0, 8.0)


def test_relative_polar():
    point = CoordinateParser.parse(
        "@10<45",
        base_point=Point(2.0, 3.0, 0.0),
    )
    expected = 10.0 / math.sqrt(2.0)
    assert_point(
        point,
        2.0 + expected,
        3.0 + expected,
    )


def test_absolute_polar():
    point = CoordinateParser.parse(
        "10<90"
    )
    assert_point(point, 0.0, 10.0)


def test_direct_distance():
    point = CoordinateParser.parse(
        "12.5",
        base_point=Point(4.5, -5.0, 0.0),
        direction_point=Point(10.0, -5.0, 0.0),
    )
    assert_point(point, 17.0, -5.0)


def test_relative_requires_base_point():
    with pytest.raises(
        CoordinateParseError
    ):
        CoordinateParser.parse(
            "@10,5"
        )
