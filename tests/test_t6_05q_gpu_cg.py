import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_cg import GPUConjugateGradientSolver
    x,r=GPUConjugateGradientSolver().solve(((4,0),(0,9)),(8,18));assert r.converged and x==pytest.approx((2,2))
