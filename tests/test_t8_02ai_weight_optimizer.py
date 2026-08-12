import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.weight_optimizer import WeightOptimizer
    assert WeightOptimizer().reduction_percent(100,80)==20
