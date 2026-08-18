import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_unity import StabilityUnity
    r=StabilityUnity().evaluate(50,100,20,100,10,100)
    assert r.maximum_unity==0.5 and r.status=='PASS'
