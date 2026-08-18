import pytest
from design.steel.base_plate_domain import *
from design.steel.base_plate_design_engine import *
@pytest.mark.parametrize("i",range(120))
def test_design(i):
    p=BasePlate("P",.5,.5,.03,250e6);c=ColumnFootprint(.25,.25)
    aa=(AnchorRod("A1",.025,AnchorGrade.F1554_55,380e6,517e6,-.15,-.15),AnchorRod("A2",.025,AnchorGrade.F1554_55,380e6,517e6,.15,.15))
    r=BasePlateDesignEngine().design(p,c,aa,BasePlateDemand(500e3,20e3),28e6,1)
    assert r.maximum_unity>=0
