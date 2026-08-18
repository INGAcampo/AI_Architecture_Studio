from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .model import TransactionState


@dataclass(slots=True)
class TransactionOperation:
    redo: Callable[[], None]
    undo: Callable[[], None]
    label: str = ""


@dataclass(slots=True)
class RegenerationTransaction:
    transaction_id: str
    name: str
    parent: "RegenerationTransaction | None" = None
    state: TransactionState = TransactionState.ACTIVE
    operations: list[TransactionOperation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("transaction_id no puede estar vacío")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")

    def add_operation(self, operation: TransactionOperation) -> None:
        if self.state is not TransactionState.ACTIVE:
            raise RuntimeError("La transacción no está activa")
        self.operations.append(operation)

    def commit(self) -> None:
        if self.state is not TransactionState.ACTIVE:
            raise RuntimeError("La transacción no está activa")
        self.state = TransactionState.COMMITTED

    def rollback(self) -> None:
        if self.state not in {TransactionState.ACTIVE, TransactionState.FAILED}:
            raise RuntimeError("La transacción no puede revertirse")
        for operation in reversed(self.operations):
            operation.undo()
        self.state = TransactionState.ROLLED_BACK
