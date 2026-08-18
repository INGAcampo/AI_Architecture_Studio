from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DryRunStep:
    step_id: str
    operation: str
    would_write_external_state: bool
    reversible: bool


@dataclass(frozen=True)
class DryRunReport:
    accepted: bool
    blocked_steps: tuple[str,...]
    reversible_steps: tuple[str,...]


def evaluate_dry_run(
    steps: tuple[DryRunStep,...],
    *,
    allow_external_writes: bool = False,
) -> DryRunReport:
    blocked=[]
    reversible=[]

    for step in steps:
        if not step.step_id.strip() or not step.operation.strip():
            raise ValueError("dry-run step identity is invalid")

        if step.reversible:
            reversible.append(step.step_id)

        if step.would_write_external_state and not allow_external_writes:
            blocked.append(step.step_id)

    return DryRunReport(
        accepted=not blocked,
        blocked_steps=tuple(blocked),
        reversible_steps=tuple(reversible),
    )
