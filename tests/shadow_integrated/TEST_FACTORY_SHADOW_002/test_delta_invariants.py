from shadow_test_factory_ext.delta import compare_failure_sets
from shadow_test_factory_ext.invariants import verify_queue_authority


def test_delta_comparison_detects_introduced_and_resolved():
    result = compare_failure_sets(
        {"old-a", "old-b"},
        {"old-b", "new-c"},
    )

    assert result.introduced == ("new-c",)
    assert result.resolved == ("old-a",)
    assert result.unchanged == ("old-b",)


def test_delta_comparison_accepts_identical_failure_sets():
    result = compare_failure_sets({"a", "b"}, {"b", "a"})
    assert result.introduced_count == 0
    assert result.resolved == ()
    assert result.unchanged == ("a", "b")


def test_queue_authority_invariant_passes_valid_ready_entries():
    result = verify_queue_authority(
        [
            {
                "megablock": "X",
                "state": "READY_FOR_RECONCILIATION",
                "integration_authorized": False,
            }
        ]
    )
    assert result.passed is True


def test_queue_authority_invariant_rejects_authority_leak():
    result = verify_queue_authority(
        [
            {
                "megablock": "X",
                "state": "READY_FOR_RECONCILIATION",
                "integration_authorized": True,
            }
        ]
    )
    assert result.passed is False
    assert "integration_authorized" in result.violations[0]
