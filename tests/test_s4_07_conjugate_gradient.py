import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.sparse_matrices import SparseMatrixCSR
from engines.numerical.conjugate_gradient import *

@pytest.mark.parametrize("i", range(120))
def test_cg(i):
    a=SparseMatrixCSR.from_triplets(2,2,((0,0,4),(0,1,1),(1,0,1),(1,1,3)))
    r=ConjugateGradientSolver().solve(a,DenseVector((1,2)))
    assert r.converged
    assert r.solution.values[0]==pytest.approx(1/11)
    assert r.solution.values[1]==pytest.approx(7/11)
