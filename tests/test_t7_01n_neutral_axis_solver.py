import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.neutral_axis_solver import NeutralAxisSolver
    assert NeutralAxisSolver().solve(1000,420,300,28)>0
