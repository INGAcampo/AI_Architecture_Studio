import pytest
from design.steel.weld_domain import *
from design.steel.groove_weld import *
@pytest.mark.parametrize("i",range(120))
def test_groove(i):
    s=WeldSegment("W",WeldType.CJP,.012,.25,0,0,.25,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert GrooveWeldEngine().calculate(s,450e6).design_capacity>0
