"""Dry-run synchronization planning and conflict policy for AIAS ↔ AutoCAD.

No AutoCAD writes are performed here. The module transforms change-detection
results into explicit, auditable sync-plan items and blocks destructive or
ambiguous actions by default.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Iterable


class RiskLevel(str, Enum):
    """Represent RiskLevel within the AIAS production BIM interoperability layer."""
    SAFE = "safe"
    REVIEW = "review"
    BLOCKED = "blocked"


class PlanAction(str, Enum):
    """Represent PlanAction within the AIAS production BIM interoperability layer."""
    NONE = "none"
    PULL_FROM_AUTOCAD = "pull_from_autocad"
    CREATE_IN_AIAS = "create_in_aias"
    REVIEW_DELETE_OR_RECREATE = "review_delete_or_recreate"
    PUSH_TO_AUTOCAD = "push_to_autocad"
    CREATE_IN_AUTOCAD = "create_in_autocad"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class SyncPolicy:
    """Default non-destructive synchronization policy."""

    allow_read_pull: bool = True
    allow_create_in_aias: bool = True
    allow_push_to_autocad: bool = False
    allow_create_in_autocad: bool = False
    allow_delete_in_aias: bool = False
    allow_delete_in_autocad: bool = False
    require_explicit_conflict_resolution: bool = True


@dataclass(frozen=True)
class SyncPlanItem:
    """Represent SyncPlanItem within the AIAS production BIM interoperability layer."""
    autocad_handle: str | None
    aias_id: str | None
    detected_state: str
    proposed_action: PlanAction
    risk: RiskLevel
    executable: bool
    reason: str
    kind: str | None = None
    layer: str | None = None


def plan_for_detection(
    detection: dict[str, Any],
    policy: SyncPolicy | None = None,
) -> SyncPlanItem:
    """Translate one detected state into a safe dry-run plan item."""
    policy = policy or SyncPolicy()
    state = str(detection.get("state") or "")
    handle = detection.get("autocad_handle")
    aias_id = detection.get("aias_id")
    kind = detection.get("kind")
    layer = detection.get("layer")

    if state == "IN_SYNC":
        return SyncPlanItem(
            handle, aias_id, state, PlanAction.NONE, RiskLevel.SAFE, True,
            "Entity is unchanged from the accepted baseline.", kind, layer
        )

    if state == "AUTOCAD_CHANGED":
        return SyncPlanItem(
            handle, aias_id, state, PlanAction.PULL_FROM_AUTOCAD,
            RiskLevel.SAFE if policy.allow_read_pull else RiskLevel.BLOCKED,
            bool(policy.allow_read_pull),
            "AutoCAD changed; read-only pull is allowed by default policy."
            if policy.allow_read_pull
            else "AutoCAD changed; pull is disabled by policy.",
            kind, layer
        )

    if state == "NEW_IN_AUTOCAD":
        return SyncPlanItem(
            handle, aias_id, state, PlanAction.CREATE_IN_AIAS,
            RiskLevel.SAFE if policy.allow_create_in_aias else RiskLevel.BLOCKED,
            bool(policy.allow_create_in_aias),
            "Entity exists only in AutoCAD; creating an AIAS-side representation is non-destructive."
            if policy.allow_create_in_aias
            else "Create-in-AIAS is disabled by policy.",
            kind, layer
        )

    if state == "MISSING_IN_AUTOCAD":
        return SyncPlanItem(
            handle, aias_id, state, PlanAction.REVIEW_DELETE_OR_RECREATE,
            RiskLevel.REVIEW,
            False,
            "Baseline identity is absent from live AutoCAD. No automatic delete or recreate is permitted.",
            kind, layer
        )

    if state in {"AIAS_CHANGED", "MISSING_IN_AIAS"}:
        action = (
            PlanAction.PUSH_TO_AUTOCAD
            if state == "AIAS_CHANGED"
            else PlanAction.CREATE_IN_AUTOCAD
        )
        allowed = (
            policy.allow_push_to_autocad
            if state == "AIAS_CHANGED"
            else policy.allow_create_in_autocad
        )
        return SyncPlanItem(
            handle, aias_id, state, action,
            RiskLevel.REVIEW if allowed else RiskLevel.BLOCKED,
            False,
            "AutoCAD write is not executable in the current dry-run stage.",
            kind, layer
        )

    if state in {"BOTH_CHANGED", "CONFLICT"}:
        return SyncPlanItem(
            handle, aias_id, state, PlanAction.CONFLICT,
            RiskLevel.BLOCKED,
            False,
            "Both sides changed or conflict is explicit; manual resolution is required.",
            kind, layer
        )

    return SyncPlanItem(
        handle, aias_id, state, PlanAction.CONFLICT,
        RiskLevel.BLOCKED,
        False,
        f"Unknown detection state {state!r}; blocked by fail-safe policy.",
        kind, layer
    )


def build_sync_plan(
    detections: Iterable[dict[str, Any]],
    policy: SyncPolicy | None = None,
) -> list[SyncPlanItem]:
    """Build a deterministic dry-run plan."""
    policy = policy or SyncPolicy()
    return [plan_for_detection(item, policy) for item in detections]


def summarize_plan(plan: Iterable[SyncPlanItem]) -> dict[str, Any]:
    """Summarize counts by action/risk/executability."""
    actions: dict[str, int] = {}
    risks: dict[str, int] = {}
    executable = 0
    blocked_or_review = 0

    items = list(plan)
    for item in items:
        actions[item.proposed_action.value] = actions.get(item.proposed_action.value, 0) + 1
        risks[item.risk.value] = risks.get(item.risk.value, 0) + 1
        if item.executable:
            executable += 1
        else:
            blocked_or_review += 1

    return {
        "total": len(items),
        "actions": actions,
        "risks": risks,
        "executable": executable,
        "blocked_or_review": blocked_or_review,
    }


def serialize_plan(plan: Iterable[SyncPlanItem]) -> list[dict[str, Any]]:
    """Execute the serialize plan operation for AIAS production BIM interoperability."""
    return [asdict(item) for item in plan]
