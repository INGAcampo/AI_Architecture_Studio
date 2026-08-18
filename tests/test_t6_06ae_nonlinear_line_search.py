import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.nonlinear_line_search import NonlinearLineSearchEngine
    assert NonlinearLineSearchEngine().backtrack(1,lambda x:(x-.5)**2)<1
