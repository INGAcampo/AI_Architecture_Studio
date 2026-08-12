"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Iterable, Mapping, Optional, Tuple

from .autocad_persistent_sync_state import (
    AIASSyncRecord,
    SyncDecision,
    SyncState,
    assess_record,
)


class OrchestratorAction(str, Enum):
    """Represent OrchestratorAction within the AIAS production BIM interoperability layer."""
    NOOP = "NOOP"
    PULL_INTO_AIAS = "PULL_INTO_AIAS"
    CREATE_AIAS_REPRESENTATION = "CREATE_AIAS_REPRESENTATION"
    BLOCKED_PUSH_TO_AUTOCAD = "BLOCKED_PUSH_TO_AUTOCAD"
    MANUAL_CONFLICT_REVIEW = "MANUAL_CONFLICT_REVIEW"
    REVIEW_MISSING_AUTOCAD_ENTITY = "REVIEW_MISSING_AUTOCAD_ENTITY"


@dataclass(frozen=True)
class PlannedSyncAction:
    """Represent PlannedSyncAction within the AIAS production BIM interoperability layer."""
    aias_id: str
    autocad_handle: str
    state: SyncState
    policy_decision: SyncDecision
    orchestrator_action: OrchestratorAction
    dry_run: bool
    autocad_write_allowed: bool
    autocad_delete_allowed: bool
    requires_manual_review: bool
    reason: str


@dataclass(frozen=True)
class SyncDryRunPlan:
    """Represent SyncDryRunPlan within the AIAS production BIM interoperability layer."""
    document_key: str
    actions: Tuple[PlannedSyncAction, ...]

    @property
    def action_count(self) -> int:
        """Execute the action count operation for this interoperability component."""
        return len(self.actions)

    def summary(self) -> Mapping[str, int]:
        """Execute the summary operation for this interoperability component."""
        result = {action.value: 0 for action in OrchestratorAction}
        for item in self.actions:
            result[item.orchestrator_action.value] += 1
        return result

    @property
    def automatic_autocad_write_count(self) -> int:
        """Execute the automatic autocad write count operation for this interoperability component."""
        return sum(1 for item in self.actions if item.autocad_write_allowed)

    @property
    def automatic_autocad_delete_count(self) -> int:
        """Execute the automatic autocad delete count operation for this interoperability component."""
        return sum(1 for item in self.actions if item.autocad_delete_allowed)

    @property
    def manual_review_count(self) -> int:
        """Execute the manual review count operation for this interoperability component."""
        return sum(1 for item in self.actions if item.requires_manual_review)


def _map_decision_to_action(
    decision: SyncDecision,
) -> Tuple[OrchestratorAction, bool, str]:
    if decision is SyncDecision.NONE:
        return OrchestratorAction.NOOP, False, "Entity is already synchronized."

    if decision is SyncDecision.PULL_FROM_AUTOCAD:
        return (
            OrchestratorAction.PULL_INTO_AIAS,
            False,
            "Dry-run permits only AIAS-side pull planning; no AutoCAD mutation.",
        )

    if decision is SyncDecision.CREATE_IN_AIAS:
        return (
            OrchestratorAction.CREATE_AIAS_REPRESENTATION,
            False,
            "Create/update only AIAS representation; AutoCAD remains read-only.",
        )

    if decision in (
        SyncDecision.PUSH_TO_AUTOCAD_BLOCKED,
        SyncDecision.CREATE_IN_AUTOCAD_BLOCKED,
    ):
        return (
            OrchestratorAction.BLOCKED_PUSH_TO_AUTOCAD,
            True,
            "AutoCAD mutation is blocked until a separate explicit production write gate.",
        )

    if decision is SyncDecision.MANUAL_CONFLICT:
        return (
            OrchestratorAction.MANUAL_CONFLICT_REVIEW,
            True,
            "Conflicting changes require manual resolution.",
        )

    if decision is SyncDecision.REVIEW_DELETE_OR_RECREATE:
        return (
            OrchestratorAction.REVIEW_MISSING_AUTOCAD_ENTITY,
            True,
            "Missing AutoCAD entity requires review; never auto-delete/recreate.",
        )

    raise ValueError(f"Unsupported policy decision: {decision}")


def plan_record(record: AIASSyncRecord) -> PlannedSyncAction:
    """Execute the plan record operation for AIAS production BIM interoperability."""
    assessment = assess_record(record)
    action, manual, reason = _map_decision_to_action(assessment.decision)

    return PlannedSyncAction(
        aias_id=assessment.aias_id,
        autocad_handle=assessment.autocad_handle,
        state=assessment.state,
        policy_decision=assessment.decision,
        orchestrator_action=action,
        dry_run=True,
        autocad_write_allowed=False,
        autocad_delete_allowed=False,
        requires_manual_review=manual,
        reason=reason,
    )


def build_dry_run_plan(
    document_key: str,
    records: Iterable[AIASSyncRecord],
) -> SyncDryRunPlan:
    """Execute the build dry run plan operation for AIAS production BIM interoperability."""
    if not document_key:
        raise ValueError("document_key is required.")

    actions = []
    seen_handles = set()
    seen_ids = set()

    for record in records:
        record.validate()
        if record.document_key != document_key:
            raise ValueError("record document_key does not match plan document_key.")

        handle = record.handle
        if handle in seen_handles:
            raise ValueError(f"Duplicate Handle in dry-run input: {handle}")
        if record.aias_id in seen_ids:
            raise ValueError(f"Duplicate AIAS ID in dry-run input: {record.aias_id}")

        item = plan_record(record)
        if not item.dry_run:
            raise RuntimeError("Orchestrator emitted a non-dry-run action.")
        if item.autocad_write_allowed or item.autocad_delete_allowed:
            raise RuntimeError("Orchestrator emitted an automatic AutoCAD mutation.")

        actions.append(item)
        seen_handles.add(handle)
        seen_ids.add(record.aias_id)

    return SyncDryRunPlan(
        document_key=document_key,
        actions=tuple(actions),
    )


def plan_to_payload(plan: SyncDryRunPlan) -> Mapping[str, object]:
    """Execute the plan to payload operation for AIAS production BIM interoperability."""
    return {
        "document_key": plan.document_key,
        "dry_run": True,
        "action_count": plan.action_count,
        "summary": plan.summary(),
        "automatic_autocad_write_count": plan.automatic_autocad_write_count,
        "automatic_autocad_delete_count": plan.automatic_autocad_delete_count,
        "manual_review_count": plan.manual_review_count,
        "actions": [
            {
                **asdict(item),
                "state": item.state.value,
                "policy_decision": item.policy_decision.value,
                "orchestrator_action": item.orchestrator_action.value,
            }
            for item in plan.actions
        ],
    }
