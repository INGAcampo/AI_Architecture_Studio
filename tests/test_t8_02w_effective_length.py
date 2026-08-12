import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.effective_length import EffectiveLengthEngine
    assert EffectiveLengthEngine().effective_length_mm(3000,1.2)==3600
