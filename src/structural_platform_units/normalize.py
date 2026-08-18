from __future__ import annotations

from dataclasses import dataclass


_FACTORS={
    ("N","N"):1.0,
    ("kN","N"):1000.0,
    ("N*m","N*m"):1.0,
    ("kN*m","N*m"):1000.0,
    ("m","m"):1.0,
    ("mm","m"):0.001,
}


@dataclass(frozen=True)
class NormalizedResult:
    value: float
    source_unit: str
    canonical_unit: str


def normalize_result_value(value: float, source_unit: str, canonical_unit: str) -> NormalizedResult:
    key=(source_unit,canonical_unit)
    if key not in _FACTORS:
        raise ValueError("unsupported unit conversion")

    return NormalizedResult(
        value=float(value)*_FACTORS[key],
        source_unit=source_unit,
        canonical_unit=canonical_unit,
    )
