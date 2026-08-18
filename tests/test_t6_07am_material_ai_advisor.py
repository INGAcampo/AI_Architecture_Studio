import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.materials.material_ai_advisor import MaterialAIAdvisor
    assert 'estable' in MaterialAIAdvisor().advise(SimpleNamespace(warnings=())).summary
