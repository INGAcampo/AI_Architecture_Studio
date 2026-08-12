import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.strength_combination import StrengthCombinationEngine
    assert StrengthCombinationEngine().combine(10,20)>=40
