import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.tension_net_rupture import TensionNetRuptureEngine
    assert TensionNetRuptureEngine().nominal_strength_n(900,400,0.9)==pytest.approx(324000)
