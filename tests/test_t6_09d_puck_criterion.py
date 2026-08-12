import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.puck_criterion import PuckCriterionEngine
    assert PuckCriterionEngine().fiber_failure(300,600,450)==pytest.approx(.5)
