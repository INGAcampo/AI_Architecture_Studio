import pytest
from engines.fem.truss import *

@pytest.mark.parametrize("i",range(120))
def test_truss(i):
    e=TrussElement(f"T{i}",("N1","N2"),(0,0,0),(3,4,0),0.01,200e9)
    k=e.local_stiffness_matrix()
    assert e.length==pytest.approx(5)
    assert k[0][0]==pytest.approx(0.01*200e9/5)
    f=e.recover_internal_forces((0,0.001))
    assert f[1]>0
