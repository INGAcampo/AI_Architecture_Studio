import pytest
from design.steel.doubler_plate import *
@pytest.mark.parametrize("i",range(120))
def test_doubler(i):
    assert DoublerPlateEngine().design(300,200,150).passed
