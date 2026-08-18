import pytest
from engines.civil.earthwork_balancing import *

@pytest.mark.parametrize("i", range(120))
def test_balance(i):
    zones = (
        EarthworkZone("A", 100+i, 20),
        EarthworkZone("B", 40, 120+i),
    )
    e = EarthworkBalancingEngine()
    cut, fill = e.totals(zones)
    assert cut == 140+i
    assert fill == 140+i
    assert e.balance(zones) == 0
