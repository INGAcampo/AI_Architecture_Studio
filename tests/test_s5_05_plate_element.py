import pytest
from engines.fem.plate import *

@pytest.mark.parametrize("i",range(120))
def test_plate(i):
    e=PlateElement4(f"P{i}",("N1","N2","N3","N4"),12,0.2,30e9,0.2,5)
    assert e.bending_rigidity()>0
    assert e.equivalent_nodal_loads()==(15.0,15.0,15.0,15.0)
    assert len(e.local_stiffness_matrix())==4
