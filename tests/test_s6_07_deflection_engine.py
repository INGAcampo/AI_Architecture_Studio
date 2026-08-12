import pytest
from engines.analysis.deflection import *

@pytest.mark.parametrize("i",range(120))
def test_deflection(i):
    e=DeflectionEngine()
    r=e.build(("N1","N2"),((0,0,0),(3,4,0)))
    assert r[1].magnitude==pytest.approx(5)
    assert e.maximum(r).node_id=="N2"
