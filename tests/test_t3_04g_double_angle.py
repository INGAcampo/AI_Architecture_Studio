import pytest
from design.steel.double_angle import *
@pytest.mark.parametrize("i",range(120))
def test_double(i):
    assert DoubleAngleEngine().design(100,80,150).passed
