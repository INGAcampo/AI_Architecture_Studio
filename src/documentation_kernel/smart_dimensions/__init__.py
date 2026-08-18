from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class DimensionPoint:
    x: float
    y: float

@dataclass(frozen=True, slots=True)
class Dimension:
    dimension_id: str
    start: DimensionPoint
    end: DimensionPoint
    prefix: str = ""
    suffix: str = ""
    precision: int = 2

    @property
    def measured_value(self):
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)

    def formatted(self):
        return f"{self.prefix}{self.measured_value:.{self.precision}f}{self.suffix}"

class SmartDimensionEngine:
    def linear(self, dimension_id, start, end, **kwargs):
        return Dimension(dimension_id, start, end, **kwargs)

    def chain_total(self, dimensions):
        return sum(item.measured_value for item in dimensions)

    def detect_duplicates(self, dimensions, tolerance=1e-9):
        seen = []
        duplicates = []
        for dimension in dimensions:
            key = round(dimension.measured_value / max(tolerance, 1e-12))
            if key in seen:
                duplicates.append(dimension.dimension_id)
            else:
                seen.append(key)
        return tuple(duplicates)
