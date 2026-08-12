import pytest
from engines.structural.steel_design import *

@pytest.mark.parametrize("index", range(120))
def test_steel_design(index):
    engine = SteelDesignEngine()
    capacity = SteelSectionCapacity(f"S{index}", 1000 + index, 500 + index, 300 + index)
    ratio = engine.interaction_ratio(100, 50, capacity)
    assert ratio > 0
    assert engine.passes(ratio, limit=2.0)
