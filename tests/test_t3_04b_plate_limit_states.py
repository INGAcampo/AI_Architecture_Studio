import pytest
from design.steel.plate_limit_states import *
@pytest.mark.parametrize("i",range(120))
def test_plate(i):
    r=PlateLimitStateEngine().calculate(.2,.012,(.024,.024),250e6,400e6)
    assert r.design_capacity>0
