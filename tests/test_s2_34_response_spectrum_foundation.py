import pytest
from engines.structural.spectrum import *

@pytest.mark.parametrize("index", range(120))
def test_spectrum(index):
    engine = ResponseSpectrumFoundation()
    points = (SpectrumPoint(0.0, 0.2), SpectrumPoint(1.0, 1.0 + index*0.01))
    value = engine.interpolate(points, 0.5)
    assert value == pytest.approx((0.2 + 1.0 + index*0.01)/2)
    assert engine.srss((3,4)) == 5
