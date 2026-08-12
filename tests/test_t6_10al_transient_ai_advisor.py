import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.transient.transient_ai_advisor import TransientAIAdvisor
    assert 'estable' in TransientAIAdvisor().advise(SimpleNamespace(warnings=())).summary
