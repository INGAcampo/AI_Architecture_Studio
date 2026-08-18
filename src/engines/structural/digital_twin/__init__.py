from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone

class AssetState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ALERT = "alert"

@dataclass(frozen=True, slots=True)
class SensorReading:
    sensor_id: str
    asset_id: str
    metric: str
    value: float
    timestamp: str

    def __post_init__(self):
        if not self.sensor_id.strip() or not self.asset_id.strip() or not self.metric.strip():
            raise ValueError("Datos obligatorios")

@dataclass(frozen=True, slots=True)
class TwinAsset:
    asset_id: str
    name: str
    state: AssetState = AssetState.ACTIVE

    def __post_init__(self):
        if not self.asset_id.strip() or not self.name.strip():
            raise ValueError("Datos obligatorios")

class DigitalTwinFoundation:
    def __init__(self):
        self.assets = {}
        self.readings = []

    def register_asset(self, asset):
        self.assets[asset.asset_id] = asset
        return asset

    def add_reading(self, reading):
        if reading.asset_id not in self.assets:
            raise KeyError(reading.asset_id)
        self.readings.append(reading)
        return reading

    def latest(self, asset_id, metric):
        matching = [
            reading for reading in self.readings
            if reading.asset_id == asset_id and reading.metric == metric
        ]
        if not matching:
            return None
        return max(matching, key=lambda reading: reading.timestamp)

    @staticmethod
    def utc_timestamp():
        return datetime.now(timezone.utc).isoformat()
