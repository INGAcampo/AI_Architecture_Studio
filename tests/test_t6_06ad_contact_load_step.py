import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_load_step import ContactLoadStep
    assert ContactLoadStep(1,1,-1e-6,0,True).converged
