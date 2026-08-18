import pytest
from engines.structural.thermal_zones import *

@pytest.mark.parametrize("index", range(120))
def test_thermal_zones(index):
    surface = EnvelopeSurface(
        f"S{index}",
        10 + index,
        0.3,
        22.0,
        10.0,
    )
    zone = ThermalZone(f"Z{index}", f"Zone {index}", 100 + index, (surface,))
    engine = ThermalZoneEngine()
    assert engine.transmission_load(zone) == pytest.approx(surface.heat_transfer)
    assert engine.air_change_load(zone, 1.0) > 0
