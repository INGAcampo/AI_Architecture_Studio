import pytest

from aias_l3_production_bim.autocad_sync_identity import (
    ExternalIdentity,
    IdentityRegistry,
    SyncAction,
    SyncPlanner,
    SyncState,
    build_baseline,
    document_key,
    fingerprint,
)


def entity(x=0.0):
    return {
        "kind": "line",
        "handle": "ABC",
        "layer": "0",
        "start": (0.0, 0.0, 0.0),
        "end": (float(x), 0.0, 0.0),
    }


def test_fingerprint_is_deterministic_and_ignores_display_state():
    a = entity(10)
    b = dict(reversed(list(a.items())))
    b["selected"] = True
    assert fingerprint(a) == fingerprint(b)


def test_document_key_is_stable():
    assert document_key(full_name=r"C:\A\B.dwg") == document_key(
        full_name=r"c:\a\b.dwg"
    )


def test_identity_registry_bidirectional_lookup():
    reg = IdentityRegistry()
    ident = ExternalIdentity("aias-1", "ab12", "doc")
    reg.bind(ident)
    assert reg.by_aias_id("aias-1") == ident
    assert reg.by_autocad_handle("doc", "AB12") == ident


def test_identity_registry_rejects_collisions():
    reg = IdentityRegistry()
    reg.bind(ExternalIdentity("aias-1", "A1", "doc"))
    with pytest.raises(ValueError):
        reg.bind(ExternalIdentity("aias-1", "B2", "doc"))
    with pytest.raises(ValueError):
        reg.bind(ExternalIdentity("aias-2", "A1", "doc"))


def test_sync_planner_in_sync():
    ident = ExternalIdentity("aias-1", "A1", "doc")
    aias = entity(10)
    acad = entity(10)
    baseline = build_baseline(ident, aias, acad)
    decision = SyncPlanner().decide(
        baseline=baseline, identity=ident, aias_entity=aias, autocad_entity=acad
    )
    assert decision.state is SyncState.IN_SYNC
    assert decision.action is SyncAction.NONE


def test_sync_planner_ai_as_changed_push():
    ident = ExternalIdentity("aias-1", "A1", "doc")
    base = entity(10)
    baseline = build_baseline(ident, base, base)
    changed = entity(20)
    decision = SyncPlanner().decide(
        baseline=baseline,
        identity=ident,
        aias_entity=changed,
        autocad_entity=base,
    )
    assert decision.state is SyncState.AIAS_CHANGED
    assert decision.action is SyncAction.PUSH_TO_AUTOCAD


def test_sync_planner_autocad_changed_pull():
    ident = ExternalIdentity("aias-1", "A1", "doc")
    base = entity(10)
    baseline = build_baseline(ident, base, base)
    changed = entity(30)
    decision = SyncPlanner().decide(
        baseline=baseline,
        identity=ident,
        aias_entity=base,
        autocad_entity=changed,
    )
    assert decision.state is SyncState.AUTOCAD_CHANGED
    assert decision.action is SyncAction.PULL_FROM_AUTOCAD


def test_sync_planner_conflict():
    ident = ExternalIdentity("aias-1", "A1", "doc")
    base = entity(10)
    baseline = build_baseline(ident, base, base)
    decision = SyncPlanner().decide(
        baseline=baseline,
        identity=ident,
        aias_entity=entity(20),
        autocad_entity=entity(30),
    )
    assert decision.state is SyncState.BOTH_CHANGED
    assert decision.action is SyncAction.CONFLICT


def test_sync_planner_missing_sides():
    planner = SyncPlanner()
    ident = ExternalIdentity("aias-1", "A1", "doc")

    left = planner.decide(
        baseline=None, identity=ident, aias_entity=None, autocad_entity=entity(10)
    )
    assert left.action is SyncAction.CREATE_IN_AIAS

    right = planner.decide(
        baseline=None, identity=ident, aias_entity=entity(10), autocad_entity=None
    )
    assert right.action is SyncAction.CREATE_IN_AUTOCAD


def test_no_baseline_different_entities_is_conflict():
    decision = SyncPlanner().decide(
        baseline=None,
        identity=None,
        aias_entity=entity(10),
        autocad_entity=entity(20),
    )
    assert decision.action is SyncAction.CONFLICT
