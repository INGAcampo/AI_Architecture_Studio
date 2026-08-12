"""Live AutoCAD reversible transaction adapter.

004AG adapts the 004AF reversible transaction contract to an already-open
temporary AutoCAD document. It does not authorize production-DWG writes.
"""
from __future__ import annotations

from typing import Any

from .autocad_write_transaction import (
    AppliedOperation,
    OperationKind,
    ReversibleWriteBackend,
    TransactionError,
    TransactionNotActive,
    WriteOperation,
)


class AutoCADTemporaryDocumentTransactionBackend:
    """Reversible backend constrained to one temporary, unsaved AutoCAD document."""

    def __init__(self, document: Any, *, pythoncom_module: Any, win32com_client_module: Any) -> None:
        self.document = document
        self.pythoncom = pythoncom_module
        self.win32com_client = win32com_client_module
        self.active_transaction: str | None = None
        self.closed = False
        self.events: list[tuple[str, str]] = []

    def _ensure_active(self) -> None:
        if self.closed:
            raise TransactionError("Temporary AutoCAD backend is already closed.")
        if self.active_transaction is None:
            raise TransactionNotActive("No active AutoCAD transaction.")

    def begin(self, transaction_id: str) -> None:
        """Execute the begin operation for this interoperability component."""
        if self.closed:
            raise TransactionError("Temporary AutoCAD backend is already closed.")
        if self.active_transaction is not None:
            raise TransactionError("AutoCAD temporary backend already has an active transaction.")
        self.active_transaction = transaction_id
        self.events.append(("begin", transaction_id))

    def apply(self, operation: WriteOperation) -> AppliedOperation:
        """Execute the apply operation for this interoperability component."""
        self._ensure_active()

        if operation.kind is not OperationKind.CREATE_LINE:
            raise NotImplementedError(
                f"004AG live sandbox supports CREATE_LINE only, got {operation.kind.value}"
            )

        start = tuple(float(x) for x in operation.payload["start"])
        end = tuple(float(x) for x in operation.payload["end"])

        if len(start) != 3 or len(end) != 3:
            raise TransactionError("AutoCAD line points must be 3D coordinates.")

        p1 = self.win32com_client.VARIANT(
            self.pythoncom.VT_ARRAY | self.pythoncom.VT_R8,
            start,
        )
        p2 = self.win32com_client.VARIANT(
            self.pythoncom.VT_ARRAY | self.pythoncom.VT_R8,
            end,
        )

        entity = self.document.ModelSpace.AddLine(p1, p2)
        handle = str(entity.Handle).upper()

        self.events.append(("create_line", handle))

        return AppliedOperation(
            operation_id=operation.operation_id,
            kind=operation.kind.value,
            result={
                "handle": handle,
                "object_name": str(entity.ObjectName),
                "layer": str(entity.Layer),
                "start": tuple(float(x) for x in entity.StartPoint),
                "end": tuple(float(x) for x in entity.EndPoint),
            },
            undo_token={
                "action": "delete_by_handle",
                "handle": handle,
            },
        )

    def rollback_operation(self, applied: AppliedOperation) -> None:
        """Execute the rollback operation operation for this interoperability component."""
        self._ensure_active()
        token = applied.undo_token

        if token.get("action") != "delete_by_handle":
            raise TransactionError(f"Unknown AutoCAD undo token: {token!r}")

        handle = str(token["handle"]).upper()
        entity = self.document.HandleToObject(handle)
        entity.Delete()
        self.events.append(("rollback_delete", handle))

    def commit(self, transaction_id: str) -> None:
        """Execute the commit operation for this interoperability component."""
        self._ensure_active()
        if self.active_transaction != transaction_id:
            raise TransactionError("AutoCAD commit transaction mismatch.")
        self.events.append(("commit", transaction_id))
        self.active_transaction = None

    def rollback(self, transaction_id: str) -> None:
        """Execute the rollback operation for this interoperability component."""
        if self.closed:
            raise TransactionError("Temporary AutoCAD backend is already closed.")
        if self.active_transaction != transaction_id:
            raise TransactionError("AutoCAD rollback transaction mismatch.")
        self.events.append(("rollback", transaction_id))
        self.active_transaction = None

    def close_without_save(self) -> None:
        """Execute the close without save operation for this interoperability component."""
        if self.active_transaction is not None:
            raise TransactionError("Cannot close AutoCAD sandbox with active transaction.")
        if not self.closed:
            self.document.Close(False)
            self.closed = True
            self.events.append(("close_without_save", ""))
