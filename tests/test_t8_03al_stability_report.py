import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_unity import StabilityResult
    from analysis.steel_stability.stability_report import StabilityReport
    assert 'PASS' in StabilityReport().build('M',StabilityResult(.5,'axial','PASS'),50)
