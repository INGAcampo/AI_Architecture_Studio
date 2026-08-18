import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.dynamic.jacobi_eigensolver import JacobiEigenSolver
    assert JacobiEigenSolver().solve(((2,0),(0,8)))[0]==(2.0,8.0)
