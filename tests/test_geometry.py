import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from engines.geometry.point import Point
from engines.geometry.line import Line
from engines.transform.transform_manager import TransformManager
from models.cad_circle import CadCircle


def test_geometry():
    p1 = Point(0, 0, 0)
    p2 = Point(3, 4, 0)

    line = Line(p1, p2)

    print("Distancia:", p1.distance_to(p2))
    print("Longitud línea:", line.length)
    print("Punto medio:", line.midpoint)

    assert p1.distance_to(p2) == 5
    assert line.length == 5
    assert line.midpoint.to_tuple() == (1.5, 2.0, 0.0)

    print("Geometry Engine OK")


def test_scale_circle():
    circle = CadCircle(Point(0, 0, 0), 2)

    TransformManager.scale_element(circle, 2.0, 0.0, 0.0, 0.0)

    assert circle.radius == 4.0


test_geometry()