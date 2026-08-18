import pytest
from design.steel.extended_end_plate import *
@pytest.mark.parametrize("i",range(120))
def test_extended(i):
    r=ExtendedEndPlateEngine().design(100e3,.5,300e3,250e3,200e3)
    assert r.bolt_row_force==pytest.approx(200e3)
