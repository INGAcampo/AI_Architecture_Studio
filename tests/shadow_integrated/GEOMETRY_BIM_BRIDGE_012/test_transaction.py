from geometry_bim_bridge_transaction.transaction import evaluate_geometry_transaction

def test_complete_geometry_transaction_is_accepted():
    d=evaluate_geometry_transaction(
        patch_guard_passed=True,
        rollback_fully_reversible=True,
        target_snapshot_available=True,
    )
    assert d.accepted is True

def test_missing_snapshot_is_blocked():
    d=evaluate_geometry_transaction(
        patch_guard_passed=True,
        rollback_fully_reversible=True,
        target_snapshot_available=False,
    )
    assert d.accepted is False
    assert d.reason=="target_snapshot_missing"

def test_nonreversible_transaction_is_blocked():
    d=evaluate_geometry_transaction(
        patch_guard_passed=True,
        rollback_fully_reversible=False,
        target_snapshot_available=True,
    )
    assert d.accepted is False
