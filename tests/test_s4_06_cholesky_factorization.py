import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.dense_matrices import DenseMatrix
from engines.numerical.cholesky import *

@pytest.mark.parametrize("i", range(120))
def test_cholesky(i):
    a=DenseMatrix(((4,1),(1,3))); b=DenseVector((1,2))
    x=CholeskyEngine().solve(a,b)
    assert x.values[0]==pytest.approx(1/11)
    assert x.values[1]==pytest.approx(7/11)
