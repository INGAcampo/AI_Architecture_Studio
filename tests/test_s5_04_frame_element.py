import pytest
from engines.fem.frame import *

@pytest.mark.parametrize("i",range(120))
def test_frame(i):
    e=FrameElement2D(f"F{i}",("N1","N2"),(0,0),(3,4),0.02,200e9,8e-6)
    assert e.length==pytest.approx(5)
    assert len(e.local_stiffness_matrix())==6
    assert e.transformation_matrix()[0][0]==pytest.approx(0.6)
