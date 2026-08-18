import pytest
from engines.analysis.internal_forces import *
from engines.fem.truss import TrussElement

@pytest.mark.parametrize("i",range(120))
def test_internal_forces(i):
    e=TrussElement(f"T{i}",("N1","N2"),(0,0,0),(1,0,0),1,100)
    r=InternalForceRecovery().recover((e,),{e.element_id:(None,0)},(0.1,))
    assert r[0].forces[1]==pytest.approx(10)
