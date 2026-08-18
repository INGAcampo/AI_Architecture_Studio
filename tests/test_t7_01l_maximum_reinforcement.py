import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.maximum_reinforcement import MaximumReinforcementEngine
    assert MaximumReinforcementEngine().area(300,500,.02)>0
