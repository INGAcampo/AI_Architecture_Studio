import pytest
from analysis.composite_steel_concrete.module_14 import Engine
@pytest.mark.parametrize("i",range(120))
def test_module(i):
 r=Engine().evaluate(); assert r.status=="PASS"; assert r.unity==pytest.approx(.5)
