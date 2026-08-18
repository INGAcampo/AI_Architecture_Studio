import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_dense_matrix import GPUDenseMatrix
    assert GPUDenseMatrix().matvec(((2,0),(0,3)),(2,2))==(4,6)
