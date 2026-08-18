from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PatchGuardDecision:
    accepted: bool
    reason: str


def evaluate_patch_guard(
    patch_plan,
    *,
    allow_destructive: bool = False,
    max_operations: int = 10000,
) -> PatchGuardDecision:
    if max_operations < 1:
        raise ValueError("max_operations must be positive")

    count=len(patch_plan.operations)

    if count > max_operations:
        return PatchGuardDecision(False,"operation_limit_exceeded")

    if patch_plan.destructive and not allow_destructive:
        return PatchGuardDecision(False,"destructive_patch_requires_authorization")

    return PatchGuardDecision(True,"accepted")
