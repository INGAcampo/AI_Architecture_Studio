import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.transient.transient_solver_pipeline import TransientSolverPipeline
    assert TransientSolverPipeline().solve_sdof((0,1),.1,1,.1,10).converged
