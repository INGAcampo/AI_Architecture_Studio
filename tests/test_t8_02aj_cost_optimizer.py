import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.cost_optimizer import CostOptimizer
    assert CostOptimizer().total_cost(100,2,1.1)==pytest.approx(220)
