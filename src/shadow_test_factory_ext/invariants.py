from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvariantResult:
    passed: bool
    violations: tuple[str, ...]


def verify_queue_authority(entries) -> InvariantResult:
    violations = []

    for entry in entries:
        name = str(entry.get("megablock", ""))
        if not name:
            violations.append("queue entry missing megablock")
            continue

        if bool(entry.get("integration_authorized", False)):
            violations.append(
                f"{name}: integration_authorized must remain false in shadow queue"
            )

        if entry.get("state") != "READY_FOR_RECONCILIATION":
            violations.append(
                f"{name}: unexpected state {entry.get('state')}"
            )

    return InvariantResult(
        passed=not violations,
        violations=tuple(violations),
    )
