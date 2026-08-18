import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_model import SteelMember
    assert SteelMember('M1',6).length_m==6
