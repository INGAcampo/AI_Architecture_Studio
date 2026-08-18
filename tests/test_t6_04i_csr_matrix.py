import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.csr_matrix import CSRMatrix
    assert CSRMatrix(2,2,((0,0,2),(1,1,3))).matvec((2,2))==(4,6)
