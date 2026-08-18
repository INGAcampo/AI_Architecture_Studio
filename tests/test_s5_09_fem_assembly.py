import pytest
from engines.fem.assembly import *
from engines.fem.beam import BeamElement2D

@pytest.mark.parametrize("i",range(120))
def test_fem_assembly(i):
    e=BeamElement2D(f"B{i}",("N1","N2"),2,200e9,1e-6,4)
    a=FEMAssemblyEngine().assemble(4,{e.element_id:(0,1,2,3)},(e,))
    assert a.stiffness.nrows==4
    assert a.loads.values[0]==pytest.approx(4)
    assert a.loads.values[2]==pytest.approx(4)
