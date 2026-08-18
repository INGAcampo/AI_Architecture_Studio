from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True, slots=True)
class TelemetrySample:
    sensor_id: str
    asset_id: str
    metric: str
    value: float
    timestamp: float

    def __post_init__(self):
        if not self.sensor_id.strip() or not self.asset_id.strip() or not self.metric.strip():
            raise ValueError("Datos obligatorios")

class SensorStreamEngine:
    def __init__(self):
        self._samples = defaultdict(list)

    def publish(self, sample):
        self._samples[(sample.asset_id, sample.metric)].append(sample)
        self._samples[(sample.asset_id, sample.metric)].sort(
            key=lambda item: item.timestamp
        )
        return sample

    def latest(self, asset_id, metric):
        samples = self._samples.get((asset_id, metric), ())
        return samples[-1] if samples else None

    def window(self, asset_id, metric, start, end):
        return tuple(
            sample for sample in self._samples.get((asset_id, metric), ())
            if start <= sample.timestamp <= end
        )

    def average(self, asset_id, metric):
        samples = self._samples.get((asset_id, metric), ())
        if not samples:
            return None
        return sum(sample.value for sample in samples) / len(samples)
