import pytest
from design.steel.base_plate_domain import *
from design.steel.base_plate_vertical_slice import *
@pytest.mark.parametrize("i",range(120))
def test_slice(i):
    p=BasePlate("P",.55,.55,.035,250e6);c=ColumnFootprint(.25,.25)
    aa=(AnchorRod("A1",.025,AnchorGrade.F1554_55,380e6,517e6,-.15,-.15),AnchorRod("A2",.025,AnchorGrade.F1554_55,380e6,517e6,.15,.15))
    r=BasePlateVerticalSlice().run(p,c,aa,BasePlateDemand(300e3,20e3),28e6,1)
    assert "# Base Plate Design Report" in r.report.markdown
