from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReconciliationExecutionEnvelope:
    canonical_head: str
    expected_canonical_head: str
    dry_run_passed: bool
    targeted_tests_passed: bool
    integration_authorized: bool
    external_write_authorized: bool


def evaluate_execution_envelope(envelope: ReconciliationExecutionEnvelope):
    if envelope.canonical_head != envelope.expected_canonical_head:
        return False,"canonical_head_drift"

    if not envelope.dry_run_passed:
        return False,"dry_run_not_passed"

    if not envelope.targeted_tests_passed:
        return False,"targeted_tests_not_passed"

    if not envelope.integration_authorized:
        return False,"integration_not_authorized"

    if envelope.external_write_authorized:
        return False,"external_write_scope_not_permitted_in_reconciliation"

    return True,"accepted"
