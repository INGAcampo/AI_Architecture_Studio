import pytest
from design.steel.base_plate_domain import *
@pytest.mark.parametrize("i",range(120))
def test_domain(i):
    p=BasePlate(f"P{i}",.45,.45,.025,250e6,PlateShape.SQUARE)
    assert p.width==pytest.approx(.45)
