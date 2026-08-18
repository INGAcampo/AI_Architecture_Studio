import pytest
from engines.structural.daylighting import *

@pytest.mark.parametrize("index", range(120))
def test_daylighting(index):
    sensor = DaylightSensor(f"S{index}", 300 + index, 300)
    engine = DaylightingEngine()
    assert sensor.compliance_ratio >= 1
    assert engine.average_illuminance((sensor,)) == 300 + index
    assert engine.compliant_count((sensor,)) == 1
