import pytest
from design.steel.weld_domain import *
@pytest.mark.parametrize("i",range(120))
def test_domain(i):
    s=WeldSegment(f"W{i}",WeldType.FILLET,.008,.2,0,0,.2,0,WeldMaterial(ElectrodeClass.E70,490e6))
    assert s.length==pytest.approx(.2)
