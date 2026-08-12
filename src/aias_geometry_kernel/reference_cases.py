"""Deterministic acceptance cases spanning geometry, transforms and intersections."""
from __future__ import annotations
import math
from .primitives import Point2D, Line2D, Circle2D, Vector2D
from .polygon import Polygon2D
from .transforms import Transform2D
from .intersections import IntersectionEngine
from .measurements import MeasurementEngine

def run_reference_cases():
    """Exercise the public kernel contract with tolerance-controlled expected values."""
    square=Polygon2D((Point2D(0,0),Point2D(2,0),Point2D(2,2),Point2D(0,2)))
    cases=[
        {"id":"GC-000001","passed":Point2D(0,0).distance_to(Point2D(3,4))==5},
        {"id":"GC-000002","passed":abs(square.area-4)<1e-12},
        {"id":"GC-000003","passed":square.centroid==Point2D(1,1)},
        {"id":"GC-000004","passed":square.contains(Point2D(1,1))},
        {"id":"GC-000005","passed":Transform2D.translation(2,3).apply(Point2D(1,1))==Point2D(3,4)},
        {"id":"GC-000006","passed":IntersectionEngine.line_line(Line2D(Point2D(0,0),Point2D(2,2)),Line2D(Point2D(0,2),Point2D(2,0)))==Point2D(1,1)},
        {"id":"GC-000007","passed":len(IntersectionEngine.line_circle(Line2D(Point2D(-2,0),Point2D(2,0)),Circle2D(Point2D(0,0),1)))==2},
        {"id":"GC-000008","passed":abs(MeasurementEngine.angle_between(Vector2D(1,0),Vector2D(0,1))-math.pi/2)<1e-12},
    ]
    return cases
