import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.hpc.hpc_ai_advisor import HPCAIAdvisor
    assert 'estable' in HPCAIAdvisor().advise(SimpleNamespace(warnings=())).summary
