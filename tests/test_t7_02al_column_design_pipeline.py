import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.rc_column_domain import RCColumnInput
    from analysis.rc_columns.column_design_pipeline import ColumnDesignPipeline
    assert ColumnDesignPipeline().design(RCColumnInput('C',450,450,3500,35,420,5000,2e6,100e6,80e6)).status=='PASS'
