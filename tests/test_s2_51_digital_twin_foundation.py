import pytest
from engines.structural.digital_twin import *

@pytest.mark.parametrize("index", range(120))
def test_digital_twin(index):
    twin = DigitalTwinFoundation()
    asset = TwinAsset(f"A{index}", f"Asset {index}")
    twin.register_asset(asset)
    reading = SensorReading(
        f"S{index}",
        asset.asset_id,
        "temperature",
        20.0 + index,
        f"2026-07-25T12:{index % 60:02d}:00+00:00",
    )
    twin.add_reading(reading)
    assert twin.latest(asset.asset_id, "temperature") is reading
