from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ResultSample:
    case_id: str
    object_id: str
    value: float
    def __post_init__(self):
        if not self.case_id.strip() or not self.object_id.strip():
            raise ValueError("Identificadores obligatorios")

class ResultEnvelopeEngine:
    def envelope(self, samples):
        if not samples:
            raise ValueError("samples no puede estar vacío")
        return {
            "maximum": max(samples, key=lambda s: s.value),
            "minimum": min(samples, key=lambda s: s.value),
            "absolute": max(samples, key=lambda s: abs(s.value)),
        }
    def weighted_sum(self, samples, factors):
        return sum(sample.value * factors.get(sample.case_id, 0.0) for sample in samples)
