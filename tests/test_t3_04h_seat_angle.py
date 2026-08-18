import pytest
from design.steel.seat_angle import *
@pytest.mark.parametrize("i",range(120))
def test_seat(i):
    assert SeatAngleEngine().design(100,200,180,220).passed
