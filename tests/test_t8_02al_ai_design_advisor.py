import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_unity_check import UnityResult
    from analysis.steel_member_design.ai_design_advisor import AiDesignAdvisor
    assert 'adequate' in AiDesignAdvisor().advise(UnityResult(.5,'axial','PASS'))
