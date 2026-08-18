import pytest
from analysis.steel_connections_design.module_20 import Engine
@pytest.mark.parametrize("i",range(120))
def test_module(i):
 r=Engine().evaluate(); assert r.status=="PASS"; assert r.unity==pytest.approx(.5)
