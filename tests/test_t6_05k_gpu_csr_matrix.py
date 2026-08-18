import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.gpu.gpu_csr_matrix import GPUCSRMatrix
    assert GPUCSRMatrix((0,1,2),(0,1),(2,3)).matvec((2,2))==(4,6)
