"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional, Tuple
import hashlib
import json
import os
import tempfile


SCHEMA = "aias.autocad.sync-state.v1"


class SyncState(str, Enum):
    """Represent SyncState within the AIAS production BIM interoperability layer."""
    IN_SYNC = "IN_SYNC"
    AIAS_CHANGED = "AIAS_CHANGED"
    AUTOCAD_CHANGED = "AUTOCAD_CHANGED"
    BOTH_CHANGED = "BOTH_CHANGED"
    MISSING_IN_AIAS = "MISSING_IN_AIAS"
    MISSING_IN_AUTOCAD = "MISSING_IN_AUTOCAD"
    NEW_IN_AUTOCAD = "NEW_IN_AUTOCAD"


class SyncDecision(str, Enum):
    """Represent SyncDecision within the AIAS production BIM interoperability layer."""
    NONE = "NONE"
    PUSH_TO_AUTOCAD_BLOCKED = "PUSH_TO_AUTOCAD_BLOCKED"
    PULL_FROM_AUTOCAD = "PULL_FROM_AUTOCAD"
    MANUAL_CONFLICT = "MANUAL_CONFLICT"
    CREATE_IN_AIAS = "CREATE_IN_AIAS"
    CREATE_IN_AUTOCAD_BLOCKED = "CREATE_IN_AUTOCAD_BLOCKED"
    REVIEW_DELETE_OR_RECREATE = "REVIEW_DELETE_OR_RECREATE"


@dataclass(frozen=True)
class AIASSyncRecord:
    """Represent AIASSyncRecord within the AIAS production BIM interoperability layer."""
    document_key: str
    aias_id: str
    autocad_handle: str
    baseline_fingerprint: str
    aias_fingerprint: Optional[str]
    autocad_fingerprint: Optional[str]

    @property
    def handle(self) -> str:
        """Execute the handle operation for this interoperability component."""
        return self.autocad_handle.upper()

    def validate(self) -> None:
        """Execute the validate operation for this interoperability component."""
        if not self.document_key:
            raise ValueError("document_key is required.")
        if not self.autocad_handle:
            raise ValueError("autocad_handle is required.")
        expected = f"autocad:{self.document_key}:{self.handle}"
        if self.aias_id != expected:
            raise ValueError(
                f"Unstable AIAS ID: expected {expected!r}, got {self.aias_id!r}."
            )
        if not self.baseline_fingerprint:
            raise ValueError("baseline_fingerprint is required.")


@dataclass(frozen=True)
class SyncAssessment:
    """Represent SyncAssessment within the AIAS production BIM interoperability layer."""
    aias_id: str
    autocad_handle: str
    state: SyncState
    decision: SyncDecision
    automatic_write_allowed: bool
    automatic_delete_allowed: bool
    reason: str


def classify_sync_state(record: AIASSyncRecord) -> SyncState:
    """Execute the classify sync state operation for AIAS production BIM interoperability."""
    record.validate()

    base = record.baseline_fingerprint
    aias = record.aias_fingerprint
    acad = record.autocad_fingerprint

    if aias is None and acad is None:
        return SyncState.BOTH_CHANGED
    if aias is None:
        return SyncState.MISSING_IN_AIAS
    if acad is None:
        return SyncState.MISSING_IN_AUTOCAD

    aias_changed = aias != base
    acad_changed = acad != base

    if not aias_changed and not acad_changed:
        return SyncState.IN_SYNC
    if aias_changed and not acad_changed:
        return SyncState.AIAS_CHANGED
    if not aias_changed and acad_changed:
        return SyncState.AUTOCAD_CHANGED
    return SyncState.BOTH_CHANGED


def policy_for_state(state: SyncState) -> Tuple[SyncDecision, bool, bool, str]:
    """Execute the policy for state operation for AIAS production BIM interoperability."""
    if state is SyncState.IN_SYNC:
        return SyncDecision.NONE, False, False, "No synchronization action required."
    if state is SyncState.AIAS_CHANGED:
        return (
            SyncDecision.PUSH_TO_AUTOCAD_BLOCKED,
            False,
            False,
            "AIAS changed; production push remains blocked pending an explicit live write gate.",
        )
    if state is SyncState.AUTOCAD_CHANGED:
        return (
            SyncDecision.PULL_FROM_AUTOCAD,
            False,
            False,
            "AutoCAD changed; safe direction is read/pull into AIAS representation.",
        )
    if state is SyncState.BOTH_CHANGED:
        return (
            SyncDecision.MANUAL_CONFLICT,
            False,
            False,
            "Both sides changed; manual conflict resolution is required.",
        )
    if state is SyncState.MISSING_IN_AIAS:
        return (
            SyncDecision.CREATE_IN_AIAS,
            False,
            False,
            "AutoCAD binding exists while AIAS representation is missing.",
        )
    if state is SyncState.MISSING_IN_AUTOCAD:
        return (
            SyncDecision.REVIEW_DELETE_OR_RECREATE,
            False,
            False,
            "AutoCAD object is missing; never delete/recreate automatically.",
        )
    if state is SyncState.NEW_IN_AUTOCAD:
        return (
            SyncDecision.CREATE_IN_AIAS,
            False,
            False,
            "New AutoCAD object should be represented in AIAS first.",
        )
    raise ValueError(f"Unsupported sync state: {state}")


def assess_record(record: AIASSyncRecord) -> SyncAssessment:
    """Execute the assess record operation for AIAS production BIM interoperability."""
    state = classify_sync_state(record)
    decision, write_allowed, delete_allowed, reason = policy_for_state(state)
    return SyncAssessment(
        aias_id=record.aias_id,
        autocad_handle=record.handle,
        state=state,
        decision=decision,
        automatic_write_allowed=write_allowed,
        automatic_delete_allowed=delete_allowed,
        reason=reason,
    )


class PersistentAIASSyncStateStore:
    """
    Persistent AIAS-side representation of per-entity sync fingerprints.

    No vendor APIs are used here. The store is designed to be fed by:
      - certified baseline/persistent identity bindings,
      - AIAS-side entity fingerprints,
      - AutoCAD readback fingerprints.

    Save semantics are atomic and tamper-evident.
    """

    def __init__(self, document_key: str) -> None:
        if not document_key:
            raise ValueError("document_key is required.")
        self.document_key = document_key
        self._records: Dict[str, AIASSyncRecord] = {}

    def __len__(self) -> int:
        return len(self._records)

    def upsert(self, record: AIASSyncRecord) -> None:
        """Execute the upsert operation for this interoperability component."""
        record.validate()
        if record.document_key != self.document_key:
            raise ValueError("record document_key does not match store.")
        self._records[record.handle] = AIASSyncRecord(
            document_key=record.document_key,
            aias_id=record.aias_id,
            autocad_handle=record.handle,
            baseline_fingerprint=record.baseline_fingerprint,
            aias_fingerprint=record.aias_fingerprint,
            autocad_fingerprint=record.autocad_fingerprint,
        )

    def get(self, handle: str) -> Optional[AIASSyncRecord]:
        """Execute the get operation for this interoperability component."""
        return self._records.get(str(handle).upper())

    def records(self) -> Tuple[AIASSyncRecord, ...]:
        """Execute the records operation for this interoperability component."""
        return tuple(self._records[h] for h in sorted(self._records))

    def assessments(self) -> Tuple[SyncAssessment, ...]:
        """Execute the assessments operation for this interoperability component."""
        return tuple(assess_record(r) for r in self.records())

    def summary(self) -> Mapping[str, int]:
        """Execute the summary operation for this interoperability component."""
        counts = {state.value: 0 for state in SyncState}
        for assessment in self.assessments():
            counts[assessment.state.value] += 1
        return counts

    def to_payload(self) -> Mapping[str, object]:
        """Execute the to payload operation for this interoperability component."""
        records = [asdict(r) for r in self.records()]
        payload = {
            "schema": SCHEMA,
            "document_key": self.document_key,
            "count": len(records),
            "records": records,
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return {
            **payload,
            "payload_sha256": hashlib.sha256(canonical).hexdigest(),
        }

    def save_atomic(self, path: Path) -> None:
        """Execute the save atomic operation for this interoperability component."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        blob = (
            json.dumps(self.to_payload(), ensure_ascii=False, indent=2, sort_keys=True)
            + "\n"
        ).encode("utf-8")

        fd, temp_name = tempfile.mkstemp(
            prefix=path.name + ".",
            suffix=".tmp",
            dir=str(path.parent),
        )
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(blob)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise

    @classmethod
    def load(cls, path: Path) -> "PersistentAIASSyncStateStore":
        """Execute the load operation for this interoperability component."""
        payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        if payload.get("schema") != SCHEMA:
            raise ValueError("Unsupported sync-state schema.")

        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError("sync-state records must be a list.")
        if payload.get("count") != len(records):
            raise ValueError("sync-state count mismatch.")

        hash_payload = {
            "schema": payload["schema"],
            "document_key": payload.get("document_key"),
            "count": payload.get("count"),
            "records": records,
        }
        canonical = json.dumps(
            hash_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        if payload.get("payload_sha256") != hashlib.sha256(canonical).hexdigest():
            raise ValueError("sync-state payload SHA-256 mismatch.")

        store = cls(str(payload.get("document_key") or ""))
        for raw in records:
            store.upsert(AIASSyncRecord(**raw))
        if len(store) != payload["count"]:
            raise ValueError("sync-state uniqueness/cardinality mismatch.")
        return store


def build_initial_sync_store_from_bindings(
    bindings_payload: Mapping[str, object],
) -> PersistentAIASSyncStateStore:
    """Execute the build initial sync store from bindings operation for AIAS production BIM interoperability."""
    document_key = str(bindings_payload.get("document_key") or "")
    records = bindings_payload.get("records")
    if not document_key or not isinstance(records, list):
        raise ValueError("Invalid persistent binding payload.")

    store = PersistentAIASSyncStateStore(document_key)
    for binding in records:
        handle = str(binding.get("autocad_handle") or "").upper()
        aias_id = str(binding.get("aias_id") or "")
        fingerprint = str(binding.get("fingerprint") or "")
        store.upsert(
            AIASSyncRecord(
                document_key=document_key,
                aias_id=aias_id,
                autocad_handle=handle,
                baseline_fingerprint=fingerprint,
                aias_fingerprint=fingerprint,
                autocad_fingerprint=fingerprint,
            )
        )
    return store
