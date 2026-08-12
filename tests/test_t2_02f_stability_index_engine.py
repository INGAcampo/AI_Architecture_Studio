import pytest
from design.steel.stability_index import StabilityIndexEngine

@pytest.mark.parametrize("i", range(120))
def test_stability_index(i):
    r=StabilityIndexEngine().calculate(f"L{i}",10e6,0.01,500e3,3.5)
    assert r.theta>0
    assert isinstance(r.stable,bool)
