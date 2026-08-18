from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SpectrumPoint:
    period: float
    acceleration: float
    def __post_init__(self):
        if self.period < 0 or self.acceleration < 0:
            raise ValueError("Datos inválidos")

class ResponseSpectrumFoundation:
    def interpolate(self, points, period):
        ordered = sorted(points, key=lambda p: p.period)
        if not ordered:
            raise ValueError("points no puede estar vacío")
        if period <= ordered[0].period:
            return ordered[0].acceleration
        if period >= ordered[-1].period:
            return ordered[-1].acceleration
        for left, right in zip(ordered, ordered[1:]):
            if left.period <= period <= right.period:
                ratio = (period-left.period)/(right.period-left.period)
                return left.acceleration + ratio*(right.acceleration-left.acceleration)
        raise RuntimeError("Interpolación fallida")
    def srss(self, values):
        return sum(v*v for v in values) ** 0.5
