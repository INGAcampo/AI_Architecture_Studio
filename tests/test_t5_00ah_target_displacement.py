import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.target_displacement import TargetDisplacementEngine
    assert TargetDisplacementEngine().calculate(1,1,1,1,1,1)>0
