import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.column_diagnostics import ColumnDiagnosticsEngine
    assert not ColumnDiagnosticsEngine().inspect(.8,50,True,True).warnings
