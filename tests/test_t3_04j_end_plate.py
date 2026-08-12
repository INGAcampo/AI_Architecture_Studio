import pytest
from design.steel.end_plate import *
@pytest.mark.parametrize("i",range(120))
def test_endplate(i):
    assert EndPlateEngine().design(10,30,20,50,15,40).passed
