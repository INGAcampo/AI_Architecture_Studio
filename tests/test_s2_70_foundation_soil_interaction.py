import pytest
from engines.structural.soil_interaction import *

@pytest.mark.parametrize("index", range(120))
def test_soil_interaction(index):
    spring = SoilSpring(f"S{index}", 10000 + index, 2)
    reaction = SoilInteractionEngine().reaction(spring, 0.01)
    assert reaction > 0
