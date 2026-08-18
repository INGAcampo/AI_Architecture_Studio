import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.fem.global_sparse_matrix import GlobalSparseMatrix
    from analysis.fem.fem_assembly import FemAssembly
    g=GlobalSparseMatrix(2);FemAssembly().assemble(g,((1,-1),(-1,1)),(0,1));assert g.get(0,0)==1
