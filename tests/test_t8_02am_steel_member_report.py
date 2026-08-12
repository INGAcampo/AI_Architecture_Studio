import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_model import SteelMember
    from analysis.steel_member_design.member_unity_check import UnityResult
    from analysis.steel_member_design.steel_member_report import SteelMemberReport
    assert 'PASS' in SteelMemberReport().build(SteelMember('M',6),UnityResult(.5,'axial','PASS'),'W')
