import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.drift_calculator import DriftCalculator
    assert round(DriftCalculator().calculate(.02,.005,3)[1],3)==.005
