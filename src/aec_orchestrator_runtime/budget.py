from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutBudget:
    total_s: float
    consumed_s: float = 0.0

    @property
    def remaining_s(self) -> float:
        return max(0.0,self.total_s-self.consumed_s)


def consume_budget(budget: TimeoutBudget, elapsed_s: float) -> TimeoutBudget:
    if budget.total_s <= 0:
        raise ValueError("total_s must be positive")
    if budget.consumed_s < 0:
        raise ValueError("consumed_s must not be negative")
    if elapsed_s < 0:
        raise ValueError("elapsed_s must not be negative")

    consumed=min(budget.total_s,budget.consumed_s+elapsed_s)
    return TimeoutBudget(total_s=budget.total_s,consumed_s=consumed)
