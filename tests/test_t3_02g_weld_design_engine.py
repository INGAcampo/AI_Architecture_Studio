import pytest
from design.steel.weld_domain import *
from design.steel.weld_design_engine import *
@pytest.mark.parametrize("i",range(120))
def test_design(i):
    s=WeldSegment("W",WeldType.FILLET,.008,.2,0,0,.2,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert WeldDesignEngine().design(s,WeldDemand(force_x=50e3)).design_capacity>0
