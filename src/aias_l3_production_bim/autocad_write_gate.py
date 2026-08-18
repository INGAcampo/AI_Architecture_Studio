"""Explicit AutoCAD write gate for isolated sandbox exercises.

004AE does not enable production DWG writes. It only authorizes a temporary,
unsaved-document exercise when the exact approval token is supplied.
"""
from __future__ import annotations

from dataclasses import dataclass


SANDBOX_APPROVAL_TOKEN = "AIAS_AUTOCAD_2027_SANDBOX_ONE_ENTITY_WRITE"


@dataclass(frozen=True)
class WriteGateDecision:
    """Result of evaluating an explicit write request."""

    approved: bool
    scope: str
    production_write_enabled: bool
    reason: str


def evaluate_write_gate(*, token: str | None, temporary_document: bool) -> WriteGateDecision:
    """Authorize only the exact temporary-document sandbox scope."""
    if token != SANDBOX_APPROVAL_TOKEN:
        return WriteGateDecision(
            approved=False,
            scope="NONE",
            production_write_enabled=False,
            reason="Exact sandbox approval token was not supplied.",
        )

    if not temporary_document:
        return WriteGateDecision(
            approved=False,
            scope="NONE",
            production_write_enabled=False,
            reason="004AE forbids writing to the production/active source drawing.",
        )

    return WriteGateDecision(
        approved=True,
        scope="TEMPORARY_UNSAVED_DOCUMENT_ONE_LINE",
        production_write_enabled=False,
        reason="Explicit token authorizes one isolated line exercise only.",
    )
