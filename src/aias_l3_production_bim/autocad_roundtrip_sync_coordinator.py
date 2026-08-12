"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Iterable, Mapping, Sequence

from .autocad_persistent_sync_state import AIASSyncRecord, SyncState, assess_record
from .autocad_sync_orchestrator import OrchestratorAction, plan_record


class CoordinationMode(str, Enum):
    """Represent CoordinationMode within the AIAS production BIM interoperability layer."""
    DRY_RUN = "DRY_RUN"


@dataclass(frozen=True)
class CoordinatedSyncItem:
    """Represent CoordinatedSyncItem within the AIAS production BIM interoperability layer."""
    document_key: str
    aias_id: str
    autocad_handle: str
    state: SyncState
    action: OrchestratorAction
    automatic_autocad_write_allowed: bool
    automatic_autocad_delete_allowed: bool
    requires_manual_review: bool

    def as_dict(self) -> dict:
        """Execute the as dict operation for this interoperability component."""
        return {
            "document_key": self.document_key,
            "aias_id": self.aias_id,
            "autocad_handle": self.autocad_handle,
            "state": self.state.value,
            "action": self.action.value,
            "automatic_autocad_write_allowed": self.automatic_autocad_write_allowed,
            "automatic_autocad_delete_allowed": self.automatic_autocad_delete_allowed,
            "requires_manual_review": self.requires_manual_review,
        }


@dataclass(frozen=True)
class ConsolidatedSyncPlan:
    """Represent ConsolidatedSyncPlan within the AIAS production BIM interoperability layer."""
    document_key: str
    mode: CoordinationMode
    items: tuple[CoordinatedSyncItem, ...]
    state_counts: Mapping[str, int]
    action_counts: Mapping[str, int]
    manual_review_count: int
    automatic_autocad_write_count: int
    automatic_autocad_delete_count: int
    plan_fingerprint: str

    @property
    def total(self) -> int:
        """Execute the total operation for this interoperability component."""
        return len(self.items)

    @property
    def is_safe_dry_run(self) -> bool:
        """Execute the is safe dry run operation for this interoperability component."""
        return (
            self.mode is CoordinationMode.DRY_RUN
            and self.automatic_autocad_write_count == 0
            and self.automatic_autocad_delete_count == 0
        )

    @property
    def has_manual_review(self) -> bool:
        """Execute the has manual review operation for this interoperability component."""
        return self.manual_review_count > 0

    def as_dict(self) -> dict:
        """Execute the as dict operation for this interoperability component."""
        return {
            "document_key": self.document_key,
            "mode": self.mode.value,
            "total": self.total,
            "state_counts": dict(self.state_counts),
            "action_counts": dict(self.action_counts),
            "manual_review_count": self.manual_review_count,
            "automatic_autocad_write_count": self.automatic_autocad_write_count,
            "automatic_autocad_delete_count": self.automatic_autocad_delete_count,
            "is_safe_dry_run": self.is_safe_dry_run,
            "has_manual_review": self.has_manual_review,
            "plan_fingerprint": self.plan_fingerprint,
            "items": [item.as_dict() for item in self.items],
        }


class RoundtripSyncCoordinator:
    """Consolidate triadic AIAS/AutoCAD sync records into a safe dry-run plan.

    NEW_IN_AUTOCAD is a discovery state that exists before an AIAS/baseline
    representation has been materialized. AIASSyncRecord permits construction
    of that discovery-shaped record, while its persistent validation contract
    intentionally requires a baseline. Therefore the coordinator recognizes
    the discovery pattern before delegating persistent records to assess_record().

    No AutoCAD COM/vendor APIs or write/delete/save surfaces are exposed here.
    """

    def __init__(self, *, mode: CoordinationMode = CoordinationMode.DRY_RUN):
        if mode is not CoordinationMode.DRY_RUN:
            raise ValueError("Only DRY_RUN coordination is supported.")
        self._mode = mode

    @property
    def mode(self) -> CoordinationMode:
        """Execute the mode operation for this interoperability component."""
        return self._mode

    @staticmethod
    def _is_new_in_autocad_discovery(record: AIASSyncRecord) -> bool:
        return (
            record.baseline_fingerprint is None
            and record.aias_fingerprint is None
            and record.autocad_fingerprint is not None
        )

    @staticmethod
    def _coordinate_one(record: AIASSyncRecord) -> CoordinatedSyncItem:
        if RoundtripSyncCoordinator._is_new_in_autocad_discovery(record):
            # Discovery-only branch: no persistent baseline exists yet, so do not
            # call AIASSyncRecord.validate()/assess_record(). The established
            # policy is to create an AIAS-side representation only.
            return CoordinatedSyncItem(
                document_key=record.document_key,
                aias_id=record.aias_id,
                autocad_handle=record.autocad_handle,
                state=SyncState.NEW_IN_AUTOCAD,
                action=OrchestratorAction.CREATE_AIAS_REPRESENTATION,
                automatic_autocad_write_allowed=False,
                automatic_autocad_delete_allowed=False,
                requires_manual_review=False,
            )

        assessment = assess_record(record)
        planned = plan_record(record)

        if planned.autocad_write_allowed:
            raise RuntimeError(
                f"Unsafe orchestrator result: automatic AutoCAD write allowed for {record.autocad_handle}."
            )
        if planned.autocad_delete_allowed:
            raise RuntimeError(
                f"Unsafe orchestrator result: automatic AutoCAD delete allowed for {record.autocad_handle}."
            )

        return CoordinatedSyncItem(
            document_key=record.document_key,
            aias_id=record.aias_id,
            autocad_handle=record.autocad_handle,
            state=assessment.state,
            action=planned.orchestrator_action,
            automatic_autocad_write_allowed=planned.autocad_write_allowed,
            automatic_autocad_delete_allowed=planned.autocad_delete_allowed,
            requires_manual_review=planned.requires_manual_review,
        )

    def coordinate(self, records: Iterable[AIASSyncRecord]) -> ConsolidatedSyncPlan:
        """Execute the coordinate operation for this interoperability component."""
        source = tuple(records)
        if not source:
            raise ValueError("At least one sync record is required.")

        document_keys = {record.document_key for record in source}
        if len(document_keys) != 1:
            raise ValueError("All sync records must belong to exactly one document.")

        handles = [record.autocad_handle for record in source]
        aias_ids = [record.aias_id for record in source]

        # Handle uniqueness is the primary AutoCAD identity invariant. Check it
        # first because duplicate Handles can naturally imply duplicate derived
        # AIAS IDs as a secondary consequence.
        if len(set(handles)) != len(handles):
            raise ValueError("Duplicate AutoCAD Handles are not allowed.")
        if len(set(aias_ids)) != len(aias_ids):
            raise ValueError("Duplicate AIAS IDs are not allowed.")

        coordinated = [
            self._coordinate_one(record)
            for record in sorted(source, key=lambda r: (r.autocad_handle, r.aias_id))
        ]

        state_counts = {state.value: 0 for state in SyncState}
        action_counts = {action.value: 0 for action in OrchestratorAction}

        for item in coordinated:
            state_counts[item.state.value] += 1
            action_counts[item.action.value] += 1

        manual_review_count = sum(item.requires_manual_review for item in coordinated)
        write_count = sum(item.automatic_autocad_write_allowed for item in coordinated)
        delete_count = sum(item.automatic_autocad_delete_allowed for item in coordinated)

        if write_count or delete_count:
            raise RuntimeError("Unsafe consolidated plan attempted automatic AutoCAD mutation.")

        document_key = next(iter(document_keys))
        fingerprint_payload = {
            "document_key": document_key,
            "mode": self._mode.value,
            "items": [item.as_dict() for item in coordinated],
        }
        plan_fingerprint = hashlib.sha256(
            json.dumps(
                fingerprint_payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()

        return ConsolidatedSyncPlan(
            document_key=document_key,
            mode=self._mode,
            items=tuple(coordinated),
            state_counts=state_counts,
            action_counts=action_counts,
            manual_review_count=manual_review_count,
            automatic_autocad_write_count=write_count,
            automatic_autocad_delete_count=delete_count,
            plan_fingerprint=plan_fingerprint,
        )


def coordinate_roundtrip_sync(records: Sequence[AIASSyncRecord]) -> ConsolidatedSyncPlan:
    """Execute the coordinate roundtrip sync operation for AIAS production BIM interoperability."""
    return RoundtripSyncCoordinator().coordinate(records)
