"""004AI controlled production one-entity exercise contract.

This module adds no autonomous production-write capability. It only defines
the exact runtime authorization contract for the explicitly approved 004AI
exercise.
"""
from __future__ import annotations

from dataclasses import dataclass

from .autocad_production_write_gate import (
    PRODUCTION_APPROVAL_TOKEN,
    ProductionWritePreflight,
    evaluate_production_write_gate,
)


@dataclass(frozen=True)
class ControlledProductionExerciseApproval:
    """Explicit authorization for one temporary production-document entity."""

    user_approved: bool
    approval_token: str
    one_entity_only: bool = True
    rollback_required: bool = True
    save_forbidden: bool = True
    send_command_forbidden: bool = True


def validate_004ai_approval(
    preflight: ProductionWritePreflight,
    approval: ControlledProductionExerciseApproval,
) -> bool:
    """Return True only for the exact 004AI authorization envelope."""
    if not approval.user_approved:
        return False
    if approval.approval_token != PRODUCTION_APPROVAL_TOKEN:
        return False
    if not approval.one_entity_only:
        return False
    if not approval.rollback_required:
        return False
    if not approval.save_forbidden:
        return False
    if not approval.send_command_forbidden:
        return False

    decision = evaluate_production_write_gate(
        preflight,
        approval_token=approval.approval_token,
        explicit_user_approval=True,
    )
    return (
        decision.authorized
        and decision.technically_eligible
        and decision.scope == "CONTROLLED_ONE_ENTITY_NO_SAVE_TRANSACTION"
        and decision.production_write_enabled is False
    )
