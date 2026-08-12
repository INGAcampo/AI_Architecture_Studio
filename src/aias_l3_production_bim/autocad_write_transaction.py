"""Reversible AutoCAD write transaction core for AIAS.

This module defines the contract and transaction semantics required before any
production-DWG write can be enabled. 004AF itself does not write to AutoCAD.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Protocol
import uuid


class TransactionState(str, Enum):
    """Represent TransactionState within the AIAS production BIM interoperability layer."""
    NEW = "new"
    ACTIVE = "active"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


class OperationKind(str, Enum):
    """Represent OperationKind within the AIAS production BIM interoperability layer."""
    CREATE_LINE = "create_line"
    DELETE_ENTITY = "delete_entity"
    UPDATE_ENTITY = "update_entity"


@dataclass(frozen=True)
class WriteOperation:
    """Represent WriteOperation within the AIAS production BIM interoperability layer."""
    kind: OperationKind
    payload: dict[str, Any]
    operation_id: str = field(default_factory=lambda: uuid.uuid4().hex)


@dataclass(frozen=True)
class AppliedOperation:
    """Represent AppliedOperation within the AIAS production BIM interoperability layer."""
    operation_id: str
    kind: str
    result: dict[str, Any]
    undo_token: dict[str, Any]


class ReversibleWriteBackend(Protocol):
    """Backend contract for reversible write execution."""

    def begin(self, transaction_id: str) -> None: """Execute the begin operation for this interoperability component."""; ...
    def apply(self, operation: WriteOperation) -> AppliedOperation: """Execute the apply operation for this interoperability component."""; ...
    def rollback_operation(self, applied: AppliedOperation) -> None: """Execute the rollback operation operation for this interoperability component."""; ...
    def commit(self, transaction_id: str) -> None: """Execute the commit operation for this interoperability component."""; ...
    def rollback(self, transaction_id: str) -> None: """Execute the rollback operation for this interoperability component."""; ...


class TransactionError(RuntimeError):
    """Represent TransactionError within the AIAS production BIM interoperability layer."""
    pass


class TransactionNotActive(TransactionError):
    """Represent TransactionNotActive within the AIAS production BIM interoperability layer."""
    pass


class TransactionAlreadyClosed(TransactionError):
    """Represent TransactionAlreadyClosed within the AIAS production BIM interoperability layer."""
    pass


class ProductionWriteDisabled(TransactionError):
    """Represent ProductionWriteDisabled within the AIAS production BIM interoperability layer."""
    pass


@dataclass
class TransactionJournalEntry:
    """Represent TransactionJournalEntry within the AIAS production BIM interoperability layer."""
    event: str
    detail: dict[str, Any]


@dataclass
class ReversibleTransaction:
    """Represent ReversibleTransaction within the AIAS production BIM interoperability layer."""
    backend: ReversibleWriteBackend
    production_write_enabled: bool = False
    transaction_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    state: TransactionState = TransactionState.NEW
    applied: list[AppliedOperation] = field(default_factory=list)
    journal: list[TransactionJournalEntry] = field(default_factory=list)

    def begin(self) -> None:
        """Execute the begin operation for this interoperability component."""
        if self.state is not TransactionState.NEW:
            raise TransactionError(f"Cannot begin transaction from {self.state.value}")
        if self.production_write_enabled:
            raise ProductionWriteDisabled(
                "004AF does not authorize production-DWG write execution."
            )
        self.backend.begin(self.transaction_id)
        self.state = TransactionState.ACTIVE
        self.journal.append(TransactionJournalEntry("BEGIN", {"transaction_id": self.transaction_id}))

    def apply(self, operation: WriteOperation) -> AppliedOperation:
        """Execute the apply operation for this interoperability component."""
        if self.state is not TransactionState.ACTIVE:
            raise TransactionNotActive("Transaction must be ACTIVE before apply().")
        try:
            applied = self.backend.apply(operation)
        except Exception as exc:
            self.state = TransactionState.FAILED
            self.journal.append(TransactionJournalEntry(
                "APPLY_FAILED",
                {"operation_id": operation.operation_id, "error": f"{type(exc).__name__}: {exc}"}
            ))
            self.rollback()
            raise
        self.applied.append(applied)
        self.journal.append(TransactionJournalEntry(
            "APPLY",
            {"operation_id": operation.operation_id, "kind": operation.kind.value}
        ))
        return applied

    def commit(self) -> None:
        """Execute the commit operation for this interoperability component."""
        if self.state is not TransactionState.ACTIVE:
            raise TransactionNotActive("Transaction must be ACTIVE before commit().")
        self.backend.commit(self.transaction_id)
        self.state = TransactionState.COMMITTED
        self.journal.append(TransactionJournalEntry("COMMIT", {"transaction_id": self.transaction_id}))

    def rollback(self) -> None:
        """Execute the rollback operation for this interoperability component."""
        if self.state in {TransactionState.COMMITTED, TransactionState.ROLLED_BACK}:
            raise TransactionAlreadyClosed(f"Transaction already {self.state.value}.")
        # reverse operation order
        for item in reversed(self.applied):
            try:
                self.backend.rollback_operation(item)
                self.journal.append(TransactionJournalEntry(
                    "ROLLBACK_OPERATION",
                    {"operation_id": item.operation_id, "kind": item.kind}
                ))
            except Exception as exc:
                self.journal.append(TransactionJournalEntry(
                    "ROLLBACK_OPERATION_FAILED",
                    {"operation_id": item.operation_id, "error": f"{type(exc).__name__}: {exc}"}
                ))
                raise
        self.backend.rollback(self.transaction_id)
        self.state = TransactionState.ROLLED_BACK
        self.journal.append(TransactionJournalEntry("ROLLBACK", {"transaction_id": self.transaction_id}))

    def to_dict(self) -> dict[str, Any]:
        """Execute the to dict operation for this interoperability component."""
        return {
            "transaction_id": self.transaction_id,
            "state": self.state.value,
            "production_write_enabled": self.production_write_enabled,
            "applied": [asdict(x) for x in self.applied],
            "journal": [asdict(x) for x in self.journal],
        }


class InMemoryReversibleBackend:
    """Deterministic reversible backend used to prove transaction semantics."""

    def __init__(self) -> None:
        self.entities: dict[str, dict[str, Any]] = {}
        self.events: list[tuple[str, str]] = []
        self.active_transaction: str | None = None

    def begin(self, transaction_id: str) -> None:
        """Execute the begin operation for this interoperability component."""
        if self.active_transaction is not None:
            raise TransactionError("Backend already has an active transaction.")
        self.active_transaction = transaction_id
        self.events.append(("begin", transaction_id))

    def apply(self, operation: WriteOperation) -> AppliedOperation:
        """Execute the apply operation for this interoperability component."""
        if self.active_transaction is None:
            raise TransactionNotActive("Backend transaction is not active.")

        if operation.kind is OperationKind.CREATE_LINE:
            entity_id = operation.payload.get("entity_id") or uuid.uuid4().hex
            if entity_id in self.entities:
                raise TransactionError(f"Entity already exists: {entity_id}")
            entity = {
                "entity_id": entity_id,
                "kind": "line",
                "start": tuple(operation.payload["start"]),
                "end": tuple(operation.payload["end"]),
            }
            self.entities[entity_id] = entity
            self.events.append(("create", entity_id))
            return AppliedOperation(
                operation_id=operation.operation_id,
                kind=operation.kind.value,
                result={"entity_id": entity_id},
                undo_token={"action": "delete", "entity_id": entity_id},
            )

        if operation.kind is OperationKind.DELETE_ENTITY:
            entity_id = operation.payload["entity_id"]
            previous = dict(self.entities[entity_id])
            del self.entities[entity_id]
            self.events.append(("delete", entity_id))
            return AppliedOperation(
                operation_id=operation.operation_id,
                kind=operation.kind.value,
                result={"entity_id": entity_id},
                undo_token={"action": "restore", "entity": previous},
            )

        raise NotImplementedError(operation.kind.value)

    def rollback_operation(self, applied: AppliedOperation) -> None:
        """Execute the rollback operation operation for this interoperability component."""
        token = applied.undo_token
        action = token["action"]
        if action == "delete":
            entity_id = token["entity_id"]
            self.entities.pop(entity_id, None)
            self.events.append(("undo_create", entity_id))
            return
        if action == "restore":
            entity = dict(token["entity"])
            self.entities[entity["entity_id"]] = entity
            self.events.append(("undo_delete", entity["entity_id"]))
            return
        raise TransactionError(f"Unknown undo action: {action}")

    def commit(self, transaction_id: str) -> None:
        """Execute the commit operation for this interoperability component."""
        if self.active_transaction != transaction_id:
            raise TransactionError("Commit transaction mismatch.")
        self.events.append(("commit", transaction_id))
        self.active_transaction = None

    def rollback(self, transaction_id: str) -> None:
        """Execute the rollback operation for this interoperability component."""
        if self.active_transaction != transaction_id:
            raise TransactionError("Rollback transaction mismatch.")
        self.events.append(("rollback", transaction_id))
        self.active_transaction = None
