import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.lrfd_core import LrfdEngine
    assert LrfdEngine().design_strength(100,0.9)==pytest.approx(90)
