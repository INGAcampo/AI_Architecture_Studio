import pytest
from engines.civil.open_channels import *

@pytest.mark.parametrize("i", range(120))
def test_channel(i):
    c = RectangularChannel(f"C{i}", 3, 1.2, 0.002, 0.015)
    e = OpenChannelHydraulicsEngine()
    assert e.area(c) == pytest.approx(3.6)
    assert e.discharge(c) > 0
