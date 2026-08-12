import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.shells.shell_ai_advisor import ShellAIAdvisor
    assert 'estable' in ShellAIAdvisor().advise(SimpleNamespace(warnings=())).summary
