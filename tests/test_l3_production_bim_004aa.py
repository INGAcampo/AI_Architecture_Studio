from aias_l3_production_bim.autocad_sync_policy import (
    PlanAction,
    RiskLevel,
    SyncPolicy,
    build_sync_plan,
    plan_for_detection,
    summarize_plan,
)


def d(state):
    return {
        "autocad_handle": "A1",
        "aias_id": "aias-1",
        "state": state,
        "kind": "line",
        "layer": "0",
    }


def test_in_sync_is_safe_noop():
    p = plan_for_detection(d("IN_SYNC"))
    assert p.proposed_action is PlanAction.NONE
    assert p.risk is RiskLevel.SAFE
    assert p.executable is True


def test_autocad_changed_allows_read_pull_only():
    p = plan_for_detection(d("AUTOCAD_CHANGED"))
    assert p.proposed_action is PlanAction.PULL_FROM_AUTOCAD
    assert p.executable is True
    assert p.risk is RiskLevel.SAFE


def test_new_in_autocad_can_create_in_aias():
    p = plan_for_detection(d("NEW_IN_AUTOCAD"))
    assert p.proposed_action is PlanAction.CREATE_IN_AIAS
    assert p.executable is True


def test_missing_in_autocad_is_never_auto_deleted():
    p = plan_for_detection(d("MISSING_IN_AUTOCAD"))
    assert p.proposed_action is PlanAction.REVIEW_DELETE_OR_RECREATE
    assert p.risk is RiskLevel.REVIEW
    assert p.executable is False


def test_write_side_actions_are_blocked_by_default():
    p1 = plan_for_detection(d("AIAS_CHANGED"))
    p2 = plan_for_detection(d("MISSING_IN_AIAS"))
    assert p1.proposed_action is PlanAction.PUSH_TO_AUTOCAD
    assert p2.proposed_action is PlanAction.CREATE_IN_AUTOCAD
    assert p1.executable is False
    assert p2.executable is False
    assert p1.risk is RiskLevel.BLOCKED
    assert p2.risk is RiskLevel.BLOCKED


def test_conflict_is_blocked():
    p = plan_for_detection(d("BOTH_CHANGED"))
    assert p.proposed_action is PlanAction.CONFLICT
    assert p.executable is False
    assert p.risk is RiskLevel.BLOCKED


def test_unknown_state_fails_safe():
    p = plan_for_detection(d("WHATEVER"))
    assert p.proposed_action is PlanAction.CONFLICT
    assert p.executable is False
    assert p.risk is RiskLevel.BLOCKED


def test_summary_counts():
    plan = build_sync_plan([
        d("IN_SYNC"),
        d("AUTOCAD_CHANGED"),
        d("NEW_IN_AUTOCAD"),
        d("MISSING_IN_AUTOCAD"),
    ])
    s = summarize_plan(plan)
    assert s["total"] == 4
    assert s["executable"] == 3
    assert s["blocked_or_review"] == 1
    assert s["actions"]["review_delete_or_recreate"] == 1


def test_policy_can_disable_pull_and_create_in_aias():
    policy = SyncPolicy(allow_read_pull=False, allow_create_in_aias=False)
    a = plan_for_detection(d("AUTOCAD_CHANGED"), policy)
    b = plan_for_detection(d("NEW_IN_AUTOCAD"), policy)
    assert a.executable is False
    assert b.executable is False
    assert a.risk is RiskLevel.BLOCKED
    assert b.risk is RiskLevel.BLOCKED
