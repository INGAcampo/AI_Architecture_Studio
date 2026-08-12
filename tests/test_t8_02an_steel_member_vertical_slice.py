import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.steel_member_vertical_slice import SteelMemberVerticalSlice
    r=SteelMemberVerticalSlice().run()
    assert r[3].status=='PASS' and 'Steel Member Design Report' in r[-1]
