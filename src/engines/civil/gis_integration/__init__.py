from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GeoFeature:
    feature_id: str
    longitude: float
    latitude: float
    properties: dict

class GisSpatialIntegration:
    def bbox(self, features):
        xs = [f.longitude for f in features]
        ys = [f.latitude for f in features]
        return min(xs), min(ys), max(xs), max(ys)

    def find_by_property(self, features, key, value):
        return tuple(f for f in features if f.properties.get(key) == value)
