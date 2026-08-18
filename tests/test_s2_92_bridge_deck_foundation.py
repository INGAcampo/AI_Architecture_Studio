import pytest
from engines.civil.bridges import *
@pytest.mark.parametrize("i",range(120))
def test_bridge(i):
    b=BridgeDeck(f"B{i}",3,30,12,0.25);e=BridgeDeckEngine()
    assert e.total_length(b)==90 and e.deck_area(b)==1080 and e.concrete_volume(b)==270
