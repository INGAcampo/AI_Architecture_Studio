import pytest
from design.steel.base_plate_domain import *
from design.steel.anchor_rod_strength import *
@pytest.mark.parametrize("i",range(120))
def test_anchor_strength(i):
    a=AnchorRod("A",.025,AnchorGrade.F1554_55,380e6,517e6,0,0)
    assert AnchorRodStrengthEngine().calculate(a).tension_capacity>0
