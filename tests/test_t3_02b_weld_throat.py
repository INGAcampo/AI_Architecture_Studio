import pytest
from design.steel.weld_domain import *
from design.steel.weld_throat import *
@pytest.mark.parametrize("i",range(120))
def test_throat(i):
    s=WeldSegment("W",WeldType.FILLET,.01,.2,0,0,.2,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert EffectiveThroatEngine().calculate(s).effective_throat==pytest.approx(.00707)
