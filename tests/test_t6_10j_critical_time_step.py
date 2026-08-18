import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.critical_time_step import CriticalTimeStepEngine
    assert CriticalTimeStepEngine().calculate(1,4)==pytest.approx(1)
