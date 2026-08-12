import pytest
from engines.numerical.vectors import DenseVector
from engines.numerical.dense_matrices import DenseMatrix
from engines.numerical.lu import *

@pytest.mark.parametrize("i", range(120))
def test_lu(i):
    a=DenseMatrix(((4,3),(6,3))); b=DenseVector((10,12))
    x=LUFactorizationEngine().solve(a,b)
    assert x.values[0]==pytest.approx(1)
    assert x.values[1]==pytest.approx(2)
