import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.dense_matrices import *

@pytest.mark.parametrize("i", range(120))
def test_dense_matrix(i):
    m=DenseMatrix(((1,2),(3,4)))
    assert m.shape==(2,2)
    assert m.transpose().rows==((1.0,3.0),(2.0,4.0))
    assert m.matvec(DenseVector((1,1))).values==(3.0,7.0)
    assert m.add(DenseMatrix.identity(2)).rows==((2.0,2.0),(3.0,5.0))
