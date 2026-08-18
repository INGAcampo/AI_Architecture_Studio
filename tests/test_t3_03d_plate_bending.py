import pytest
from design.steel.base_plate_domain import *
from design.steel.plate_bending import *
@pytest.mark.parametrize("i",range(120))
def test_bending(i):
    r=PlateBendingEngine().calculate(BasePlate("P",.5,.5,.03,250e6),ColumnFootprint(.25,.25),2e6)
    assert r.required_thickness>0
