from geometry_bim_bridge_patch.patch import PatchOperation,PatchPlan
from geometry_bim_bridge_patch_guard.guard import evaluate_patch_guard
from geometry_bim_bridge_patch_guard.fingerprint import patch_plan_sha256


def test_non_destructive_patch_is_accepted():
    plan=PatchPlan((PatchOperation("ADD","A"),),False)
    d=evaluate_patch_guard(plan)
    assert d.accepted is True


def test_destructive_patch_is_blocked_by_default():
    plan=PatchPlan((PatchOperation("REMOVE","A"),),True)
    d=evaluate_patch_guard(plan)
    assert d.accepted is False
    assert d.reason=="destructive_patch_requires_authorization"


def test_patch_fingerprint_is_deterministic():
    plan=PatchPlan(
        (
            PatchOperation("ADD","A"),
            PatchOperation("UPDATE_GEOMETRY","B"),
        ),
        False,
    )
    a=patch_plan_sha256(plan)
    b=patch_plan_sha256(plan)
    assert a==b
    assert len(a)==64


def test_operation_limit_fails_closed():
    plan=PatchPlan(
        (
            PatchOperation("ADD","A"),
            PatchOperation("ADD","B"),
        ),
        False,
    )
    d=evaluate_patch_guard(plan,max_operations=1)
    assert d.accepted is False
    assert d.reason=="operation_limit_exceeded"
