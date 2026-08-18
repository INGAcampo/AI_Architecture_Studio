import pytest
from design.steel.weld_domain import *
from design.steel.weld_design_engine import *
from design.steel.weld_optimizer import *
@pytest.mark.parametrize("i",range(120))
def test_opt(i):
    s=WeldSegment("W",WeldType.FILLET,.012,.25,0,0,.25,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert WeldOptimizer(WeldDesignEngine()).optimize(s,WeldDemand(force_x=40e3)).recommended_size is not None
