from __future__ import annotations


def classify_for_queue(
    *,
    targeted_tests_pass: bool,
    manifest_valid: bool,
    collision_count: int,
    integration_authorized: bool,
) -> str:
    if integration_authorized:
        return "INVALID_AUTHORITY_STATE"

    if collision_count < 0:
        raise ValueError("collision_count must not be negative")

    if not targeted_tests_pass:
        return "BLOCKED_TEST_FAILURE"

    if not manifest_valid:
        return "BLOCKED_MANIFEST_FAILURE"

    if collision_count > 0:
        return "BLOCKED_COLLISION"

    return "READY_FOR_RECONCILIATION"
