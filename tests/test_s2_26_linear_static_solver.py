import pytest
from engines.structural.solver import *
@pytest.mark.parametrize("index", range(120))
def test_solver(index):
    k1=index+1
    k2=index+2
    solver=LinearStaticSolver()
    u=solver.solve(((k1,0),(0,k2)),(k1,k2))
    assert u == pytest.approx((1,1))
    assert solver.reactions(((k1,0),(0,k2)),u,(k1,k2)) == pytest.approx((0,0))
