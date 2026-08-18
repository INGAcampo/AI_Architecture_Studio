import pytest
from engines.civil.multimodal import *
@pytest.mark.parametrize("i",range(120))
def test_multimodal(i):
    modes=(CorridorMode(TransportMode.ROAD,7),CorridorMode(TransportMode.BIKE,3))
    e=MultimodalCorridorEngine()
    assert e.total_width(modes)==10 and e.modal_share(modes,TransportMode.BIKE)==0.3
