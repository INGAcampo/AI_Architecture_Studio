import pytest
from engines.structural.systems.constraints import *

@pytest.mark.parametrize("i",range(120))
def test_constraints(i):
    e=StructuralConstraintSolver()
    r=e.solve({"x":5},(("positive",lambda o:o["x"]>0,"x must be positive"),))
    assert r.satisfied and r.violations==()
    assert e.aligned((0,0,0),(0,0,0))
