"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

@dataclass(slots=True)
class Transaction:
    """Execute the public Transaction operation for the Omega application core and shared runtime services using explicit caller inputs."""
    name: str
    undo_steps: list[Callable[[], None]] = field(default_factory=list)
    redo_steps: list[Callable[[], None]] = field(default_factory=list)

    def undo(self) -> None:
        """Execute the public Transaction.undo operation for the Omega application core and shared runtime services using explicit caller inputs."""
        for step in reversed(self.undo_steps):
            step()

    def redo(self) -> None:
        """Execute the public Transaction.redo operation for the Omega application core and shared runtime services using explicit caller inputs."""
        for step in self.redo_steps:
            step()

class TransactionManager:
    """Execute the public TransactionManager operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._undo: list[Transaction] = []
        self._redo: list[Transaction] = []

    def commit(self, transaction: Transaction) -> None:
        """Execute the public TransactionManager.commit operation for the Omega application core and shared runtime services using explicit caller inputs."""
        self._undo.append(transaction)
        self._redo.clear()

    def undo(self) -> bool:
        """Execute the public TransactionManager.undo operation for the Omega application core and shared runtime services using explicit caller inputs."""
        if not self._undo:
            return False
        transaction = self._undo.pop()
        transaction.undo()
        self._redo.append(transaction)
        return True

    def redo(self) -> bool:
        """Execute the public TransactionManager.redo operation for the Omega application core and shared runtime services using explicit caller inputs."""
        if not self._redo:
            return False
        transaction = self._redo.pop()
        transaction.redo()
        self._undo.append(transaction)
        return True
