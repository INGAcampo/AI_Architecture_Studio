import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.minimum_reinforcement import MinimumReinforcementEngine
    assert MinimumReinforcementEngine().area(300,500,28,420)>0
