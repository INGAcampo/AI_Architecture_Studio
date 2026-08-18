import pytest
from design.steel.top_seat_angle import *
@pytest.mark.parametrize("i",range(120))
def test_topseat(i):
    assert TopSeatAngleEngine().design(50,100,20,50,10,40).passed
