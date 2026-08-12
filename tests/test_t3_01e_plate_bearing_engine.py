import pytest
from design.steel.plate_bearing import PlateBearingEngine

@pytest.mark.parametrize("i", range(120))
def test_plate_bearing(i):
    r=PlateBearingEngine().calculate(0.022,0.012,450e6,0.04,0.07)
    assert r.design_capacity>0
