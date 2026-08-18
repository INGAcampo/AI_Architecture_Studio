import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.performance_evaluation import PerformanceEvaluationEngine
    assert PerformanceEvaluationEngine().classify(.02,.01,.03,.05)=='Life Safety'
