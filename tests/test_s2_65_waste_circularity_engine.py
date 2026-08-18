import pytest
from engines.structural.circularity import *

@pytest.mark.parametrize("index", range(120))
def test_circularity(index):
    flow = MaterialFlow(f"F{index}", 100 + index, reused_mass=20, recycled_mass=30)
    rate = CircularityEngine().diversion_rate(flow)
    assert 0 < rate <= 1
