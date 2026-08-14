from shadow_test_factory.queue import classify_for_queue


def test_queue_ready_requires_all_internal_gates():
    state = classify_for_queue(
        targeted_tests_pass=True,
        manifest_valid=True,
        collision_count=0,
        integration_authorized=False,
    )
    assert state == "READY_FOR_RECONCILIATION"


def test_queue_blocks_test_failure():
    assert classify_for_queue(
        targeted_tests_pass=False,
        manifest_valid=True,
        collision_count=0,
        integration_authorized=False,
    ) == "BLOCKED_TEST_FAILURE"


def test_queue_blocks_collision():
    assert classify_for_queue(
        targeted_tests_pass=True,
        manifest_valid=True,
        collision_count=2,
        integration_authorized=False,
    ) == "BLOCKED_COLLISION"


def test_queue_rejects_integration_authority_leak():
    assert classify_for_queue(
        targeted_tests_pass=True,
        manifest_valid=True,
        collision_count=0,
        integration_authorized=True,
    ) == "INVALID_AUTHORITY_STATE"
