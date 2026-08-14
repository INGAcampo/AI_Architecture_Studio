from geometry_bim_bridge_sync.plan import SyncAction,SyncPlan
from geometry_bim_bridge_patch.patch import compile_patch_plan

def test_patch_plan_preserves_order():
    p=compile_patch_plan(SyncPlan((SyncAction("ADD","A"),SyncAction("UPDATE_GEOMETRY","B"))))
    assert tuple((x.op,x.instance_id) for x in p.operations)==(("ADD","A"),("UPDATE_GEOMETRY","B"))
    assert p.destructive is False

def test_remove_marks_plan_destructive():
    p=compile_patch_plan(SyncPlan((SyncAction("REMOVE","A"),)))
    assert p.destructive is True

def test_unknown_action_fails_closed():
    try:
        compile_patch_plan(SyncPlan((SyncAction("BAD","A"),)))
    except ValueError:
        return
    assert False
