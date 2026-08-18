import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_stability.stability_unity import StabilityResult
    from analysis.steel_stability.ai_stability_advisor import AiStabilityAdvisor
    assert 'adequate' in AiStabilityAdvisor().advise(StabilityResult(.5,'axial','PASS'))
