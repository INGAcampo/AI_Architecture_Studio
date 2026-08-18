import pytest
from design.steel.connection_cost import *
@pytest.mark.parametrize("i",range(120))
def test_cost(i):
    assert ConnectionCostEngine().estimate(10,2,4,5,1,10,2,20).total_cost==pytest.approx(90)
