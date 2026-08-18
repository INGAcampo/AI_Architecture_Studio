import pytest
from analysis.high_rise_steel_buildings.module_19 import Engine
@pytest.mark.parametrize("i",range(120))
def test_module(i):
 r=Engine().evaluate(); assert r.status=="PASS"; assert r.unity==pytest.approx(.5)
