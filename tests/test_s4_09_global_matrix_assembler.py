import pytest
from engines.numerical.assembly import *
from engines.numerical.vectors import DenseVector

@pytest.mark.parametrize("i", range(120))
def test_assembly(i):
    c=ElementMatrixContribution((0,1),((2,-2),(-2,2)))
    k=GlobalMatrixAssembler().assemble(2,(c,))
    assert k.matvec(DenseVector((1,0))).values==(2.0,-2.0)
    assert k.nnz==4
