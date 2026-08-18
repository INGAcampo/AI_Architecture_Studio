import pytest
from design.steel.fin_plate import *
@pytest.mark.parametrize("i",range(120))
def test_fin(i):
    assert FinPlateDesignEngine().design(100,200,180,220).passed
