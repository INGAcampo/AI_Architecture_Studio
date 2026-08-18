import pytest
from design.steel.base_plate_domain import *
from design.steel.anchor_group import *
@pytest.mark.parametrize("i",range(120))
def test_group(i):
    aa=(AnchorRod("A1",.025,AnchorGrade.F1554_55,380e6,517e6,-.15,-.15),AnchorRod("A2",.025,AnchorGrade.F1554_55,380e6,517e6,.15,.15))
    assert len(AnchorGroupEngine().distribute(aa,BasePlateDemand(100e3,20e3)))==2
