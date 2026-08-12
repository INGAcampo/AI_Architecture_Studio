import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.global_sparse_matrix import GlobalSparseMatrix
    m=GlobalSparseMatrix(2);m.add(0,0,2);assert m.get(0,0)==2
