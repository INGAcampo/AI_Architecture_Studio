import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.p_delta_amplification import StabilityEngine
    e=StabilityEngine()
    assert e.euler_load(200000,1e8,1,3000)>0
    assert e.slenderness(1,6000,120)==50
    assert e.check(50,100).status=='PASS'
