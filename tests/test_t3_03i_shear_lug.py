import pytest
from design.steel.shear_lug import *
@pytest.mark.parametrize("i",range(120))
def test_lug(i):
    r=ShearLugEngine().calculate(.2,.2,.02,250e6,28e6,50e3)
    assert r.design_capacity>0
