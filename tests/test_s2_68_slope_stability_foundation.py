import pytest
from engines.structural.slope_stability import *

@pytest.mark.parametrize("index", range(120))
def test_slope_stability(index):
    item = SlopeSlice(f"S{index}", 100 + index, 40, 10, 30)
    factor = SlopeStabilityEngine().factor_of_safety((item,))
    assert factor > 0
