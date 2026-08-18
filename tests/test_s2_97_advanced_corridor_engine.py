import pytest
from engines.civil.advanced_corridor import *

@pytest.mark.parametrize("i", range(120))
def test_corridor(i):
    a = CorridorStation(0, 100, 7)
    b = CorridorStation(100, 110, 9)
    e = AdvancedCorridorEngine()
    mid = e.interpolate(a, b, 50)
    assert mid.elevation == 105
    assert mid.width == 8
    assert e.corridor_length((a,b)) == 100
