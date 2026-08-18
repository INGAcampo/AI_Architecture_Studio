import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.beam_optimizer import BeamOptimizer
    assert BeamOptimizer().lightest_feasible(({'utilization':.8,'serviceable':True,'concrete_volume':1,'steel_mass':100},)) is not None
