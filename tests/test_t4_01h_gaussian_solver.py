import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.gaussian_solver import GaussianSolver
    assert GaussianSolver().solve(((2,0),(0,4)),(4,8))==(2,2)
