import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.nonlinear.nonlinear_ai_advisor import NonlinearAIAdvisor
    assert 'estable' in NonlinearAIAdvisor().advise(SimpleNamespace(warnings=())).summary
