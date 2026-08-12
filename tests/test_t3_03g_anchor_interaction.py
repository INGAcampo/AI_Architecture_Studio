import pytest
from design.steel.anchor_interaction import *
@pytest.mark.parametrize("i",range(120))
def test_interaction(i):
    r=AnchorInteractionEngine().calculate(30,100,40,100)
    assert r.interaction_ratio==pytest.approx(.25)
