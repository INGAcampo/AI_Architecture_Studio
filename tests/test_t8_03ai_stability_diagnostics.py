import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_unity import StabilityResult
    from analysis.steel_stability.stability_diagnostics import StabilityDiagnostics
    assert StabilityDiagnostics().messages(StabilityResult(.5,'axial','PASS'),50)[0]=='Stable.'
