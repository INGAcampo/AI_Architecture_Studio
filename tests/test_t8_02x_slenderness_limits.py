import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.slenderness_limits import SlendernessEngine
    assert SlendernessEngine().ratio(1,3000,50)==60
