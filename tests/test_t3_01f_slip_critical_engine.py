import pytest
from design.steel.slip_critical import SlipCriticalEngine

@pytest.mark.parametrize("i", range(120))
def test_slip_critical(i):
    r=SlipCriticalEngine().calculate(125e3,0.30,2)
    assert r.design_capacity==pytest.approx(75e3)
