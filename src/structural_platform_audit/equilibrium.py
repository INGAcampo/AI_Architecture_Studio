from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EquilibriumAudit:
    applied_n: float
    reaction_n: float
    residual_n: float
    tolerance_n: float
    passed: bool


def audit_force_equilibrium(
    applied_n: float,
    reaction_n: float,
    tolerance_n: float = 1e-6,
) -> EquilibriumAudit:
    if tolerance_n < 0:
        raise ValueError("tolerance_n must not be negative")

    residual=float(applied_n)+float(reaction_n)

    return EquilibriumAudit(
        applied_n=float(applied_n),
        reaction_n=float(reaction_n),
        residual_n=residual,
        tolerance_n=float(tolerance_n),
        passed=abs(residual) <= tolerance_n,
    )
