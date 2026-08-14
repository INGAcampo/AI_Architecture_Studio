from geometry_bim_bridge_diff.diff import SceneChangeSet
from geometry_bim_bridge_sync.plan import build_sync_plan


def test_sync_plan_orders_remove_add_update():
    changes=SceneChangeSet(
        added=("new",),
        removed=("old",),
        geometry_changed=("g",),
        metadata_changed=("m",),
        unchanged=("same",),
    )
    plan=build_sync_plan(changes)

    assert tuple((a.action,a.instance_id) for a in plan.actions)==(
        ("REMOVE","old"),
        ("ADD","new"),
        ("UPDATE_GEOMETRY","g"),
        ("UPDATE_METADATA","m"),
    )


def test_geometry_change_suppresses_duplicate_metadata_update():
    changes=SceneChangeSet(
        added=(),
        removed=(),
        geometry_changed=("x",),
        metadata_changed=("x",),
        unchanged=(),
    )
    plan=build_sync_plan(changes)
    assert tuple(a.action for a in plan.actions)==("UPDATE_GEOMETRY",)


def test_empty_change_set_produces_empty_plan():
    changes=SceneChangeSet((),(),(),(),())
    assert build_sync_plan(changes).actions==()
