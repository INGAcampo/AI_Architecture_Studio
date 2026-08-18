import pytest
from design.steel.shear_tab import *
@pytest.mark.parametrize("i",range(120))
def test_tab(i):
    r=ShearTabEngine().design(100e3,.05,250e3,20e3)
    assert r.demand_moment==pytest.approx(5e3)
