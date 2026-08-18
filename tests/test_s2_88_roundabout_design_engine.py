import pytest
from engines.civil.roundabouts import *
@pytest.mark.parametrize("i",range(120))
def test_roundabout(i):
    r=Roundabout(f"R{i}",40,20,4);e=RoundaboutDesignEngine()
    assert e.circulatory_width(r)==10
    assert e.central_island_area(r)>0
