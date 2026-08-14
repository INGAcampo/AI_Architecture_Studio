from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicabilityContext:
    jurisdiction: str
    project_type: str
    effective_date: str | None = None


@dataclass(frozen=True)
class ApplicabilityDecision:
    applicable: bool
    reason: str


def evaluate_applicability(pack, context: ApplicabilityContext) -> ApplicabilityDecision:
    if not context.jurisdiction.strip():
        raise ValueError("jurisdiction must not be empty")
    if not context.project_type.strip():
        raise ValueError("project_type must not be empty")

    if pack.provenance.jurisdiction != context.jurisdiction:
        return ApplicabilityDecision(False,"jurisdiction_mismatch")

    if (
        context.effective_date
        and pack.provenance.effective_date
        and context.effective_date < pack.provenance.effective_date
    ):
        return ApplicabilityDecision(False,"project_date_before_effective_date")

    return ApplicabilityDecision(True,"applicable")
