import pytest
from design.steel.concrete_breakout import *
@pytest.mark.parametrize("i",range(120))
def test_breakout(i):
    r=ConcreteBreakoutEngine().calculate(28e6,.35,.20,20e3,10e3)
    assert r.tension_capacity>0
