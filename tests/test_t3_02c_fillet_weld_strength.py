import pytest
from design.steel.weld_domain import *
from design.steel.fillet_weld_strength import *
@pytest.mark.parametrize("i",range(120))
def test_strength(i):
    s=WeldSegment("W",WeldType.FILLET,.008,.2,0,0,.2,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert FilletWeldStrengthEngine().calculate(s).design_capacity>0
