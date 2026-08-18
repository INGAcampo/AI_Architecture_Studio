import pytest
from design.steel.weld_combined_stress import *
@pytest.mark.parametrize("i",range(120))
def test_combined(i): assert CombinedWeldStressEngine().calculate(50e3,20e3,.001,200e6).ratio>0
