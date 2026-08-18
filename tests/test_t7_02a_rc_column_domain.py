import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.rc_column_domain import RCColumnInput
    assert RCColumnInput('C',1,1,1,1,1,1,1,1,1).width==1
