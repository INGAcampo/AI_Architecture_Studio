import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.rc.rc_ai_advisor import RCAIAdvisor
    assert 'cumple' in RCAIAdvisor().advise(SimpleNamespace(warnings=())).summary
