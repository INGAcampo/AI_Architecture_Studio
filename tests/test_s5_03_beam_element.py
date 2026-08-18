import pytest
from engines.fem.beam import *

@pytest.mark.parametrize("i",range(120))
def test_beam_element(i):
    e=BeamElement2D(f"B{i}",("N1","N2"),6,200e9,8e-6,10)
    k=e.local_stiffness_matrix()
    assert len(k)==4 and len(k[0])==4
    loads=e.equivalent_nodal_loads()
    assert loads[0]==pytest.approx(30)
    assert loads[2]==pytest.approx(30)
