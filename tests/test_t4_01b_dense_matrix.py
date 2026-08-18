import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.dense_matrix import DenseMatrix
    assert DenseMatrix(((2,0),(0,3))).matvec((2,2))==(4,6)
