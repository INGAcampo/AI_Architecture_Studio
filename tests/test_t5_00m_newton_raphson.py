import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.nonlinear.newton_raphson import NewtonRaphsonSolver
    x,_,ok=NewtonRaphsonSolver().solve(lambda x:x*x-4,lambda x:2*x,1)
    assert ok and round(x,6)==2
