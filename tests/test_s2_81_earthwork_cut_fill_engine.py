import pytest
from engines.civil.earthwork import *

@pytest.mark.parametrize("index", range(120))
def test_earthwork(index):
    cells = (
        EarthworkCell("CUT", 100, 101 + index, 100 + index),
        EarthworkCell("FILL", 100, 99 + index, 100 + index),
    )
    engine = EarthworkEngine()
    assert engine.cut_volume(cells) == 100
    assert engine.fill_volume(cells) == 100
    assert engine.net_volume(cells) == 0
