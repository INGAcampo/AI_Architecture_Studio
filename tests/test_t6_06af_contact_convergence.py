import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_convergence import ContactConvergenceEngine
    assert ContactConvergenceEngine().check(1e-9,1e-7)
