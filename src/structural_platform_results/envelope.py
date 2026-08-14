from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScalarResult:
    source_case: str
    value: float


@dataclass(frozen=True)
class ResultEnvelope:
    minimum: ScalarResult
    maximum: ScalarResult
    absolute_governing: ScalarResult


def envelope_results(results) -> ResultEnvelope:
    values=tuple(results)
    if not values:
        raise ValueError("result envelope requires at least one result")

    minimum=min(values,key=lambda item:item.value)
    maximum=max(values,key=lambda item:item.value)
    absolute_governing=max(values,key=lambda item:abs(item.value))

    return ResultEnvelope(
        minimum=minimum,
        maximum=maximum,
        absolute_governing=absolute_governing,
    )
