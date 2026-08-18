import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.jacobi_preconditioner import JacobiPreconditioner
    assert JacobiPreconditioner().build(((2,0),(0,4)))==pytest.approx((.5,.25))
