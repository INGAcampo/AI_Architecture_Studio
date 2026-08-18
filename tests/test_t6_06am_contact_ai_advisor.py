import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.contact.contact_ai_advisor import ContactAIAdvisor
    assert 'estable' in ContactAIAdvisor().advise(SimpleNamespace(warnings=())).summary
