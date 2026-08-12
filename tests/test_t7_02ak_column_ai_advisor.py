import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from types import SimpleNamespace
    from analysis.rc_columns.column_ai_advisor import ColumnAIAdvisor
    assert 'cumple' in ColumnAIAdvisor().advise(SimpleNamespace(warnings=())).summary
