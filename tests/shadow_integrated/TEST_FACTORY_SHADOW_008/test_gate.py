from shadow_test_factory_checkpoint.gate import check_checkpoint_readiness

def test_all_green_is_ready():
    r=check_checkpoint_readiness(
        queue_audit_passed=True,
        dependency_closure_passed=True,
        manifest_integrity_passed=True,
        canonical_tracked_clean=True,
    )
    assert r.ready is True

def test_dirty_canonical_is_not_ready():
    r=check_checkpoint_readiness(
        queue_audit_passed=True,
        dependency_closure_passed=True,
        manifest_integrity_passed=True,
        canonical_tracked_clean=False,
    )
    assert r.ready is False
    assert r.reasons==("canonical_not_tracked_clean",)
