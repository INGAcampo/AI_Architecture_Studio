"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Protocol, Tuple


class MutationKind(str, Enum):
    """Represent MutationKind within the AIAS production BIM interoperability layer."""
    UPDATE_ENTITY = "UPDATE_ENTITY"
    DELETE_ENTITY = "DELETE_ENTITY"


class MutationState(str, Enum):
    """Represent MutationState within the AIAS production BIM interoperability layer."""
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    COMMITTED = "COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"
    FAILED = "FAILED"


@dataclass(frozen=True)
class EntitySnapshot:
    """Represent EntitySnapshot within the AIAS production BIM interoperability layer."""
    handle: str
    object_name: str
    layer: str
    geometry: Mapping[str, Any]
    properties: Mapping[str, Any]


@dataclass(frozen=True)
class UndoToken:
    """Represent UndoToken within the AIAS production BIM interoperability layer."""
    kind: MutationKind
    handle: str
    snapshot: EntitySnapshot


@dataclass(frozen=True)
class JournalEntry:
    """Represent JournalEntry within the AIAS production BIM interoperability layer."""
    event: str
    kind: Optional[MutationKind] = None
    handle: Optional[str] = None
    detail: Optional[str] = None


class ControlledMutationBackend(Protocol):
    """Represent ControlledMutationBackend within the AIAS production BIM interoperability layer."""
    def snapshot(self, handle: str) -> EntitySnapshot:
        """Execute the snapshot operation for this interoperability component."""
        ...

    def update_entity(self, handle: str, changes: Mapping[str, Any]) -> None:
        """Execute the update entity operation for this interoperability component."""
        ...

    def delete_entity(self, handle: str) -> None:
        """Execute the delete entity operation for this interoperability component."""
        ...

    def restore_entity(self, snapshot: EntitySnapshot) -> None:
        """Execute the restore entity operation for this interoperability component."""
        ...


class ControlledMutationTransaction:
    """
    Reversible UPDATE/DELETE transaction core.

    The transaction is backend-agnostic and intentionally contains no AutoCAD
    COM calls. Live vendor backends must implement ControlledMutationBackend.

    Safety invariants:
    - every mutation snapshots the exact pre-state first;
    - every successful mutation records an undo token;
    - rollback is reverse-order;
    - failure during apply triggers automatic rollback;
    - production persistence is outside this contract;
    - Save/SaveAs/SendCommand are not part of the interface.
    """

    def __init__(self, backend: ControlledMutationBackend) -> None:
        self._backend = backend
        self.state = MutationState.NEW
        self._undo: List[UndoToken] = []
        self.journal: List[JournalEntry] = []

    @property
    def undo_tokens(self) -> Tuple[UndoToken, ...]:
        """Execute the undo tokens operation for this interoperability component."""
        return tuple(self._undo)

    def begin(self) -> None:
        """Execute the begin operation for this interoperability component."""
        if self.state is not MutationState.NEW:
            raise RuntimeError(f"Cannot begin transaction from state {self.state}.")
        self.state = MutationState.ACTIVE
        self.journal.append(JournalEntry("BEGIN"))

    def update(self, handle: str, changes: Mapping[str, Any]) -> UndoToken:
        """Execute the update operation for this interoperability component."""
        self._require_active()
        if not changes:
            raise ValueError("UPDATE_ENTITY requires at least one change.")

        snapshot = self._backend.snapshot(handle)
        token = UndoToken(MutationKind.UPDATE_ENTITY, handle, snapshot)

        try:
            self._backend.update_entity(handle, changes)
        except Exception:
            self.state = MutationState.FAILED
            self.journal.append(
                JournalEntry("APPLY_FAILED", MutationKind.UPDATE_ENTITY, handle)
            )
            self._automatic_rollback()
            raise

        self._undo.append(token)
        self.journal.append(JournalEntry("APPLY", MutationKind.UPDATE_ENTITY, handle))
        return token

    def delete(self, handle: str) -> UndoToken:
        """Execute the delete operation for this interoperability component."""
        self._require_active()
        snapshot = self._backend.snapshot(handle)
        token = UndoToken(MutationKind.DELETE_ENTITY, handle, snapshot)

        try:
            self._backend.delete_entity(handle)
        except Exception:
            self.state = MutationState.FAILED
            self.journal.append(
                JournalEntry("APPLY_FAILED", MutationKind.DELETE_ENTITY, handle)
            )
            self._automatic_rollback()
            raise

        self._undo.append(token)
        self.journal.append(JournalEntry("APPLY", MutationKind.DELETE_ENTITY, handle))
        return token

    def rollback(self) -> None:
        """Execute the rollback operation for this interoperability component."""
        if self.state not in (MutationState.ACTIVE, MutationState.FAILED):
            raise RuntimeError(f"Cannot rollback transaction from state {self.state}.")
        self._rollback_tokens()
        self.state = MutationState.ROLLED_BACK
        self.journal.append(JournalEntry("ROLLBACK"))

    def commit(self) -> None:
        """Execute the commit operation for this interoperability component."""
        self._require_active()
        self.state = MutationState.COMMITTED
        self.journal.append(JournalEntry("COMMIT"))

    def _automatic_rollback(self) -> None:
        try:
            self._rollback_tokens()
        finally:
            self.state = MutationState.ROLLED_BACK
            self.journal.append(JournalEntry("ROLLBACK"))

    def _rollback_tokens(self) -> None:
        while self._undo:
            token = self._undo.pop()
            self._backend.restore_entity(token.snapshot)
            self.journal.append(
                JournalEntry("ROLLBACK_OPERATION", token.kind, token.handle)
            )

    def _require_active(self) -> None:
        if self.state is not MutationState.ACTIVE:
            raise RuntimeError(f"Transaction is not ACTIVE: {self.state}.")


class InMemoryControlledMutationBackend:
    """
    Deterministic test backend for transaction semantics.

    Entities are stored as dictionaries:
      {
        "object_name": "AcDbLine",
        "layer": "0",
        "geometry": {...},
        "properties": {...},
      }
    """

    def __init__(self, entities: Mapping[str, Mapping[str, Any]]) -> None:
        self.entities: Dict[str, Dict[str, Any]] = {
            str(h).upper(): self._clone_entity(v)
            for h, v in entities.items()
        }
        self.fail_next_update = False
        self.fail_next_delete = False

    def snapshot(self, handle: str) -> EntitySnapshot:
        """Execute the snapshot operation for this interoperability component."""
        h = str(handle).upper()
        if h not in self.entities:
            raise KeyError(h)
        e = self.entities[h]
        return EntitySnapshot(
            handle=h,
            object_name=str(e["object_name"]),
            layer=str(e["layer"]),
            geometry=dict(e.get("geometry", {})),
            properties=dict(e.get("properties", {})),
        )

    def update_entity(self, handle: str, changes: Mapping[str, Any]) -> None:
        """Execute the update entity operation for this interoperability component."""
        h = str(handle).upper()
        if self.fail_next_update:
            self.fail_next_update = False
            raise RuntimeError("Injected update failure.")
        if h not in self.entities:
            raise KeyError(h)

        entity = self.entities[h]
        for key, value in changes.items():
            if key == "layer":
                entity["layer"] = value
            elif key == "geometry":
                entity["geometry"] = dict(value)
            elif key == "properties":
                entity["properties"] = dict(value)
            else:
                raise ValueError(f"Unsupported update field: {key}")

    def delete_entity(self, handle: str) -> None:
        """Execute the delete entity operation for this interoperability component."""
        h = str(handle).upper()
        if self.fail_next_delete:
            self.fail_next_delete = False
            raise RuntimeError("Injected delete failure.")
        if h not in self.entities:
            raise KeyError(h)
        del self.entities[h]

    def restore_entity(self, snapshot: EntitySnapshot) -> None:
        """Execute the restore entity operation for this interoperability component."""
        self.entities[snapshot.handle] = {
            "object_name": snapshot.object_name,
            "layer": snapshot.layer,
            "geometry": dict(snapshot.geometry),
            "properties": dict(snapshot.properties),
        }

    @staticmethod
    def _clone_entity(entity: Mapping[str, Any]) -> Dict[str, Any]:
        return {
            "object_name": str(entity["object_name"]),
            "layer": str(entity["layer"]),
            "geometry": dict(entity.get("geometry", {})),
            "properties": dict(entity.get("properties", {})),
        }
