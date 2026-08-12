import pytest
from design.steel.concrete_bearing import *
@pytest.mark.parametrize("i",range(120))
def test_concrete(i):
    r=ConcreteBearingEngine().calculate(28e6,.25,1.0,500e3)
    assert r.design_capacity>0 and r.confinement_factor<=2
