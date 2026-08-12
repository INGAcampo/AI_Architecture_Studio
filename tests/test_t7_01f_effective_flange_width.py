import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.effective_flange_width import EffectiveFlangeWidthEngine
    assert EffectiveFlangeWidthEngine().calculate(6000,300,100)==1500
