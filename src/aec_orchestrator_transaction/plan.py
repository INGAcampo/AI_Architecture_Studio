from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TransactionState(str,Enum):
    CREATED="CREATED"
    PREPARED="PREPARED"
    EXECUTED="EXECUTED"
    COMMITTED="COMMITTED"
    ROLLED_BACK="ROLLED_BACK"
    FAILED="FAILED"


@dataclass(frozen=True)
class TransactionStep:
    step_id: str
    operation: str
    reversible: bool

    def validate(self):
        if not self.step_id.strip():
            raise ValueError("step_id must not be empty")
        if not self.operation.strip():
            raise ValueError("operation must not be empty")


@dataclass(frozen=True)
class TransactionPlan:
    transaction_id: str
    steps: tuple[TransactionStep,...]
    require_all_reversible: bool = True

    def validate(self):
        if not self.transaction_id.strip():
            raise ValueError("transaction_id must not be empty")
        if not self.steps:
            raise ValueError("transaction requires steps")

        ids=[step.step_id for step in self.steps]
        if len(ids)!=len(set(ids)):
            raise ValueError("duplicate step_id")

        for step in self.steps:
            step.validate()

        if self.require_all_reversible and any(not step.reversible for step in self.steps):
            raise ValueError("nonreversible step is not allowed by transaction plan")
