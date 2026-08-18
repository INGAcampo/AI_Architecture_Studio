import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.dynamic.dynamic_ai_advisor import DynamicAIAdvisor
    assert 'estable' in DynamicAIAdvisor().advise(SimpleNamespace(warnings=())).summary
