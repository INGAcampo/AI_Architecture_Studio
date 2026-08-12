import pytest
from design.steel.continuity_plate import *
@pytest.mark.parametrize("i",range(120))
def test_continuity(i):
    r=ContinuityPlateEngine().design(300,200,150)
    assert r.required and r.passed
