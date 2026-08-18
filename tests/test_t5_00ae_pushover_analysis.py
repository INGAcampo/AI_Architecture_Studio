import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.pushover_analysis import PushoverAnalysisEngine
    r=PushoverAnalysisEngine().run(1000,10,.05,.05)
    assert r.converged and len(r.steps)==20
