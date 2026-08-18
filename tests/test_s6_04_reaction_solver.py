import pytest
from engines.analysis.reactions import *

@pytest.mark.parametrize("i",range(120))
def test_reactions(i):
    K=((100,-100),(-100,100))
    u=(0,0.1)
    f=(0,10)
    r=ReactionSolver().calculate(K,u,f,(0,))
    assert r[0].value==pytest.approx(-10)
    assert ReactionSolver().equilibrium(r,(10,))
