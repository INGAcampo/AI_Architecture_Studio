import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.nonlinear_domain import NonlinearStep
    assert NonlinearStep(1,1,.01,0,True).converged
