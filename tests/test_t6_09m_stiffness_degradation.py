import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.stiffness_degradation import StiffnessDegradationEngine
    assert StiffnessDegradationEngine().degrade(100,.2)==pytest.approx(80)
