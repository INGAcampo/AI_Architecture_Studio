import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.pushover_analysis import PushoverAnalysisEngine
    from analysis.nonlinear.nonlinear_diagnostics import NonlinearDiagnosticsEngine
    r=PushoverAnalysisEngine().run(1000,10,.05,.05)
    assert not NonlinearDiagnosticsEngine().inspect(r).warnings
