import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.fem_solver import FemSolver
    assert FemSolver().solve(((2,0),(0,4)),(4,8)).displacements==(2.0,2.0)
