import pytest
from engines.structural.solar import *

@pytest.mark.parametrize("index", range(120))
def test_solar(index):
    surface = SolarSurface(f"S{index}", 10 + index, 500, 30, 0.8)
    energy = SolarExposureEngine().incident_energy(surface)
    assert energy > 0
