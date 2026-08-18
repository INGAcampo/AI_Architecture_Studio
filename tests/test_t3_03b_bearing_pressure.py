import pytest
from design.steel.base_plate_domain import *
from design.steel.bearing_pressure import *
@pytest.mark.parametrize("i",range(120))
def test_bearing(i):
    r=BearingPressureEngine().calculate(BasePlate("P",.5,.5,.025,250e6),BasePlateDemand(500e3,moment_x=10e3))
    assert r.maximum_pressure>=r.average_pressure
