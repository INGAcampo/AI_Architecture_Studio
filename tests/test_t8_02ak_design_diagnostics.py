import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.member_unity_check import UnityResult
    from analysis.steel_member_design.design_diagnostics import DesignDiagnostics
    assert 'reserve' in DesignDiagnostics().messages(UnityResult(.5,'axial','PASS'))[0]
