import pytest
from engines.civil.intersections import *
@pytest.mark.parametrize("i",range(120))
def test_intersections(i):
    arms=(IntersectionArm("A",3.5,3.5,90),IntersectionArm("B",4,4,90))
    e=IntersectionGeometryEngine()
    assert e.total_paved_width(arms)==15
    assert e.average_angle(arms)==90
