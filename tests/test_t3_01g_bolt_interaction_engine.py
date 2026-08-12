import pytest
from design.steel.bolt_interaction import BoltInteractionEngine

@pytest.mark.parametrize("i", range(120))
def test_interaction(i):
    r=BoltInteractionEngine().calculate(50,100,30,100)
    assert r.interaction_ratio==pytest.approx(0.34)
    assert r.passed
