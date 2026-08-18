import pytest
from engines.structural.assembly import *
@pytest.mark.parametrize("index", range(120))
def test_assembly(index):
    k=index+1
    assembler=GlobalStiffnessAssembler(3)
    matrix=assembler.add_element((0,2),((k,-k),(-k,k)))
    assert matrix[0][0] == k
    assert matrix[2][2] == k
    assert matrix[0][2] == -k
