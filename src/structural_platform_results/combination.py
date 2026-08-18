from __future__ import annotations

from dataclasses import dataclass

from .envelope import ScalarResult


@dataclass(frozen=True)
class CombinationFactor:
    case_name: str
    factor: float


def combine_scalar_results(
    values_by_case: dict[str,float],
    factors: tuple[CombinationFactor,...],
    combination_name: str,
) -> ScalarResult:
    if not combination_name.strip():
        raise ValueError("combination_name must not be empty")
    if not factors:
        raise ValueError("combination requires factors")

    total=0.0
    for item in factors:
        if item.case_name not in values_by_case:
            raise KeyError(item.case_name)
        total += values_by_case[item.case_name]*item.factor

    return ScalarResult(
        source_case=combination_name,
        value=total,
    )
