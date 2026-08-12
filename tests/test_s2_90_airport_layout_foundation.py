import pytest
from engines.civil.airport import *
@pytest.mark.parametrize("i",range(120))
def test_airport(i):
    r=Runway(f"RW{i}",2500,45,90);e=AirportLayoutEngine()
    assert e.runway_area(r)==112500 and e.total_runway_area((r,))==112500
