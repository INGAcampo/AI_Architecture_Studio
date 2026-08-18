import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_demands import MemberDemands
    from analysis.steel_member_design.member_capacity import MemberCapacity
    from analysis.steel_member_design.member_unity_check import MemberUnityCheck
    r=MemberUnityCheck().evaluate(MemberDemands(50,20,10,5),MemberCapacity(100,100,100,100))
    assert r.maximum_unity==pytest.approx(.5) and r.status=='PASS'
