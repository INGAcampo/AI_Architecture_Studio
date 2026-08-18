import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.convergence_criteria import ConvergenceCriteria
    assert ConvergenceCriteria().check(1e-7,1e-7)
