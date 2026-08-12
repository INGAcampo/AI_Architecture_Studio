import pytest
from engines.fem.contract import *

class Dummy:
    element_id="E"
    node_ids=("N1","N2")
    def local_stiffness_matrix(self): return ((1,-1),(-1,1))
    def transformation_matrix(self): return ((1,0),(0,1))
    def equivalent_nodal_loads(self): return (0,0)
    def recover_internal_forces(self,d): return d

@pytest.mark.parametrize("i",range(120))
def test_contract(i):
    d=Dummy()
    assert isinstance(d,FiniteElement)
    assert FiniteElementValidator().validate(d)==()
