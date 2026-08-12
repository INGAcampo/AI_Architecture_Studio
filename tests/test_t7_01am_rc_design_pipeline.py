import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rc_domain import RCBeamInput
    from analysis.rc.rc_design_pipeline import RCDesignPipeline
    assert RCDesignPipeline().design(RCBeamInput('B',300,550,500,28,420,180e6,120e3)).steel_area>0
