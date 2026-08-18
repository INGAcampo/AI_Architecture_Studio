import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_demands import MemberDemands
    assert MemberDemands(10).axial_n==10
