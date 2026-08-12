import pytest
from design.steel.base_plate_domain import *
from design.steel.base_plate_design_engine import *
from design.steel.base_plate_optimizer import *

@pytest.mark.parametrize("i",range(120))
def test_opt(i):
    plate=BasePlate("P",.70,.70,.060,250e6)
    column=ColumnFootprint(.25,.25)
    anchors=(
        AnchorRod("A1",.025,AnchorGrade.F1554_55,380e6,517e6,-.15,-.15),
        AnchorRod("A2",.025,AnchorGrade.F1554_55,380e6,517e6,.15,.15),
    )
    result=BasePlateOptimizer(BasePlateDesignEngine()).optimize(
        plate,column,anchors,BasePlateDemand(100e3),28e6,1.0
    )
    assert result.recommended_dimensions is not None
