import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.sparse_matrices import *

@pytest.mark.parametrize("i", range(120))
def test_sparse(i):
    m=SparseMatrixCSR.from_triplets(3,3,((0,0,2),(1,1,3),(2,2,4),(0,2,1)))
    assert m.nnz==4
    assert m.matvec(DenseVector((1,2,3))).values==(5.0,6.0,12.0)
