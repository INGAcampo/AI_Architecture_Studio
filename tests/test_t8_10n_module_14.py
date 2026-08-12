import pytest
from analysis.complete_steel_professional_workflow.module_14 import Engine
@pytest.mark.parametrize("i",range(120))
def test_module(i):
 r=Engine().evaluate(); assert r.status=="PASS"; assert r.unity==pytest.approx(.5)
