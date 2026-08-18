"""Controlled production-write gate for AutoCAD 2027.

004AH defines authorization requirements only. It never enables production
write by itself and performs no AutoCAD mutations.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


PRODUCTION_APPROVAL_TOKEN = "AIAS_AUTOCAD_2027_CONTROLLED_PRODUCTION_ONE_ENTITY_WRITE"


@dataclass(frozen=True)
class ProductionWritePreflight:
    """Represent ProductionWritePreflight within the AIAS production BIM interoperability layer."""
    exact_document_match: bool
    modelspace_parity: bool
    read_only: bool
    physical_path_present: bool
    undo_mark_supported: bool
    saved_state_known: bool
    baseline_entity_count: int
    live_entity_count: int

    @property
    def technically_eligible(self) -> bool:
        """Execute the technically eligible operation for this interoperability component."""
        return (
            self.exact_document_match
            and self.modelspace_parity
            and not self.read_only
            and self.physical_path_present
            and self.undo_mark_supported
            and self.saved_state_known
        )


@dataclass(frozen=True)
class ProductionWriteGateDecision:
    """Represent ProductionWriteGateDecision within the AIAS production BIM interoperability layer."""
    authorized: bool
    technically_eligible: bool
    production_write_enabled: bool
    scope: str
    reason: str
    requirements: dict[str, Any]


def evaluate_production_write_gate(
    preflight: ProductionWritePreflight,
    *,
    approval_token: str | None = None,
    explicit_user_approval: bool = False,
) -> ProductionWriteGateDecision:
    """Evaluate a production-write request without performing any write."""
    requirements = {
        "exact_document_match": preflight.exact_document_match,
        "modelspace_parity": preflight.modelspace_parity,
        "read_only": preflight.read_only,
        "physical_path_present": preflight.physical_path_present,
        "undo_mark_supported": preflight.undo_mark_supported,
        "saved_state_known": preflight.saved_state_known,
        "baseline_entity_count": preflight.baseline_entity_count,
        "live_entity_count": preflight.live_entity_count,
        "explicit_user_approval": explicit_user_approval,
        "approval_token_valid": approval_token == PRODUCTION_APPROVAL_TOKEN,
    }

    if not preflight.technically_eligible:
        return ProductionWriteGateDecision(
            authorized=False,
            technically_eligible=False,
            production_write_enabled=False,
            scope="NONE",
            reason="Technical production-write preflight is not clean.",
            requirements=requirements,
        )

    if not explicit_user_approval:
        return ProductionWriteGateDecision(
            authorized=False,
            technically_eligible=True,
            production_write_enabled=False,
            scope="PREFLIGHT_ONLY",
            reason="Explicit user approval is required before production write.",
            requirements=requirements,
        )

    if approval_token != PRODUCTION_APPROVAL_TOKEN:
        return ProductionWriteGateDecision(
            authorized=False,
            technically_eligible=True,
            production_write_enabled=False,
            scope="PREFLIGHT_ONLY",
            reason="Exact production approval token was not supplied.",
            requirements=requirements,
        )

    # Even with explicit approval, 004AH itself still does not enable execution.
    return ProductionWriteGateDecision(
        authorized=True,
        technically_eligible=True,
        production_write_enabled=False,
        scope="CONTROLLED_ONE_ENTITY_NO_SAVE_TRANSACTION",
        reason=(
            "Approval contract is satisfied. Execution must occur in a later, "
            "separate stage with independent runtime safeguards."
        ),
        requirements=requirements,
    )


def serialize_preflight(value: ProductionWritePreflight) -> dict[str, Any]:
    """Execute the serialize preflight operation for AIAS production BIM interoperability."""
    return asdict(value)
