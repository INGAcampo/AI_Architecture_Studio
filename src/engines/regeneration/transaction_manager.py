from __future__ import annotations

from contextlib import contextmanager
from uuid import uuid4

from .model import TransactionState
from .transaction import RegenerationTransaction, TransactionOperation


class TransactionManager:
    def __init__(self) -> None:
        self._stack: list[RegenerationTransaction] = []
        self._history: list[RegenerationTransaction] = []

    @property
    def current(self) -> RegenerationTransaction | None:
        return self._stack[-1] if self._stack else None

    def begin(self, name: str) -> RegenerationTransaction:
        transaction = RegenerationTransaction(
            str(uuid4()),
            name,
            parent=self.current,
        )
        self._stack.append(transaction)
        return transaction

    def add_operation(self, operation: TransactionOperation) -> None:
        current = self.current
        if current is None:
            raise RuntimeError("No hay una transacción activa")
        current.add_operation(operation)

    def commit(self) -> RegenerationTransaction:
        current = self.current
        if current is None:
            raise RuntimeError("No hay una transacción activa")
        self._stack.pop()
        current.commit()

        if current.parent is not None:
            current.parent.operations.extend(current.operations)
        else:
            self._history.append(current)
        return current

    def rollback(self) -> RegenerationTransaction:
        current = self.current
        if current is None:
            raise RuntimeError("No hay una transacción activa")
        self._stack.pop()
        current.rollback()
        return current

    @contextmanager
    def transaction(self, name: str):
        transaction = self.begin(name)
        try:
            yield transaction
        except Exception:
            transaction.state = TransactionState.FAILED
            self.rollback()
            raise
        else:
            self.commit()

    def history(self) -> tuple[RegenerationTransaction, ...]:
        return tuple(self._history)
