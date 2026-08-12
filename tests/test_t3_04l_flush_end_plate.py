import pytest
from design.steel.flush_end_plate import *
@pytest.mark.parametrize("i",range(120))
def test_flush(i):
    assert FlushEndPlateEngine().design(50,.5,200,150).unity_ratio>0
