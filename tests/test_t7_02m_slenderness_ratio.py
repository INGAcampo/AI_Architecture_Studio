import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc_columns.slenderness_ratio import SlendernessRatioEngine
    assert SlendernessRatioEngine().calculate(1,3000,100)==30
