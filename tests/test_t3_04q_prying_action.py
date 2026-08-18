import pytest
from design.steel.prying_action import *
@pytest.mark.parametrize("i",range(120))
def test_prying(i):
    r=PryingActionEngine().calculate(50,0.2,100)
    assert r.total_bolt_tension==pytest.approx(60)
