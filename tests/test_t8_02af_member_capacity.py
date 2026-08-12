import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_capacity import MemberCapacity
    assert MemberCapacity(1,2,3,4).mx_nmm==2
