import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.matrix.sparse_matrix import SparseMatrix
    from analysis.matrix.matrix_assembly import MatrixAssemblyEngine
    g=SparseMatrix(2);MatrixAssemblyEngine().assemble(g,((1,-1),(-1,1)),(0,1));assert g.get(0,0)==1
