import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.rc_column_domain import RCColumnInput,RCColumnResult
    from analysis.rc_columns.column_report import ColumnReportEngine
    c=RCColumnInput('C',1,1,1,1,1,1,1,1,1);r=RCColumnResult(1,1,1,.5,20,'PASS');assert 'Reinforced Concrete Column Design' in ColumnReportEngine().build(c,r).markdown
