import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.cg_solver import ConjugateGradientSolver
    x,r=ConjugateGradientSolver().solve(((4,0),(0,9)),(8,18));assert r.converged and x==pytest.approx((2,2))
