from __future__ import annotations

from dataclasses import dataclass

from .plan import TransactionPlan,TransactionState


@dataclass(frozen=True)
class TransactionResult:
    transaction_id: str
    state: TransactionState
    completed_steps: tuple[str,...]
    error: str | None = None


class TransactionEngine:
    def execute(self,plan:TransactionPlan,handlers:dict) -> TransactionResult:
        try:
            plan.validate()
        except Exception as exc:
            return TransactionResult(
                plan.transaction_id,
                TransactionState.FAILED,
                (),
                f"{type(exc).__name__}: {exc}",
            )

        completed=[]

        for step in plan.steps:
            handler=handlers.get(step.operation)
            if handler is None:
                return TransactionResult(
                    plan.transaction_id,
                    TransactionState.FAILED,
                    tuple(completed),
                    "missing handler",
                )

            try:
                handler()
            except Exception as exc:
                return TransactionResult(
                    plan.transaction_id,
                    TransactionState.ROLLED_BACK if completed else TransactionState.FAILED,
                    tuple(completed),
                    f"{type(exc).__name__}: {exc}",
                )

            completed.append(step.step_id)

        return TransactionResult(
            plan.transaction_id,
            TransactionState.COMMITTED,
            tuple(completed),
            None,
        )
