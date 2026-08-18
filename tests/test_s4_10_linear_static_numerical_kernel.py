import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.sparse_matrices import SparseMatrixCSR
from engines.numerical.linear_static import *

@pytest.mark.parametrize("i", range(120))
def test_linear_static(i):
    k=SparseMatrixCSR.from_triplets(2,2,((0,0,4),(0,1,1),(1,0,1),(1,1,3)))
    r=LinearStaticNumericalKernel().solve(k,DenseVector((1,2)))
    assert r.displacements.values[0]==pytest.approx(1/11)
    assert r.displacements.values[1]==pytest.approx(7/11)
    assert LinearStaticNumericalKernel().equilibrium_ok(r)
