import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.column_section import ColumnSection
    assert ColumnSection(400,500).area()==200000
