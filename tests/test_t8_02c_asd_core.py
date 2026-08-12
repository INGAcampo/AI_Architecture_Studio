import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.asd_core import AsdEngine
    assert AsdEngine().allowable_strength(167,1.67)==pytest.approx(100)
