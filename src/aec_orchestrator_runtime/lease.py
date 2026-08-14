from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerLease:
    worker_id: str
    issued_at_s: float
    ttl_s: float

    def validate(self):
        if not self.worker_id.strip():
            raise ValueError("worker_id must not be empty")
        if self.ttl_s <= 0:
            raise ValueError("ttl_s must be positive")


@dataclass(frozen=True)
class LeaseDecision:
    valid: bool
    remaining_s: float
    reason: str


def evaluate_lease(lease: WorkerLease, now_s: float) -> LeaseDecision:
    lease.validate()

    elapsed=float(now_s)-float(lease.issued_at_s)
    remaining=float(lease.ttl_s)-elapsed

    if elapsed < 0:
        return LeaseDecision(False,0.0,"clock_before_lease_issue")

    if remaining <= 0:
        return LeaseDecision(False,0.0,"lease_expired")

    return LeaseDecision(True,remaining,"lease_valid")
