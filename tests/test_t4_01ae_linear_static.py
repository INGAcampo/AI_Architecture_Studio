import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.linear_static import LinearStaticSolver
    assert LinearStaticSolver().solve(((2,0),(0,4)),(4,8)).converged
