import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.invariant_engine import StressInvariantEngine
    assert StressInvariantEngine().mean_stress((3,3,3,0,0,0))==3
