from __future__ import annotations

import inspect

import pytest

from aias_l3_production_bim.autocad_persistent_sync_state import (
    AIASSyncRecord,
    SyncState,
)
from aias_l3_production_bim.autocad_sync_orchestrator import OrchestratorAction
from aias_l3_production_bim.autocad_roundtrip_sync_coordinator import (
    CoordinationMode,
    RoundtripSyncCoordinator,
    coordinate_roundtrip_sync,
)

DOC = "ae5cbab8b358879e9c4c6d75"
BASE = "base"


def rec(handle, *, base=BASE, aias=BASE, acad=BASE, aias_id=None):
    return AIASSyncRecord(
        document_key=DOC,
        aias_id=aias_id or f"autocad:{DOC}:{handle}",
        autocad_handle=handle,
        baseline_fingerprint=base,
        aias_fingerprint=aias,
        autocad_fingerprint=acad,
    )


def test_in_sync_noop():
    p = coordinate_roundtrip_sync([rec("A")])
    assert p.items[0].state is SyncState.IN_SYNC
    assert p.items[0].action is OrchestratorAction.NOOP
    assert p.is_safe_dry_run


def test_aias_changed_blocked_push():
    p = coordinate_roundtrip_sync([rec("A", aias="aias-changed")])
    i = p.items[0]
    assert i.state is SyncState.AIAS_CHANGED
    assert i.action is OrchestratorAction.BLOCKED_PUSH_TO_AUTOCAD
    assert i.requires_manual_review


def test_autocad_changed_pull_into_aias():
    p = coordinate_roundtrip_sync([rec("A", acad="autocad-changed")])
    i = p.items[0]
    assert i.state is SyncState.AUTOCAD_CHANGED
    assert i.action is OrchestratorAction.PULL_INTO_AIAS
    assert not i.requires_manual_review


def test_both_changed_manual_conflict():
    p = coordinate_roundtrip_sync([rec("A", aias="aias-x", acad="acad-y")])
    i = p.items[0]
    assert i.state is SyncState.BOTH_CHANGED
    assert i.action is OrchestratorAction.MANUAL_CONFLICT_REVIEW
    assert i.requires_manual_review


def test_missing_in_aias_creates_aias_representation():
    p = coordinate_roundtrip_sync([rec("A", aias=None)])
    i = p.items[0]
    assert i.state is SyncState.MISSING_IN_AIAS
    assert i.action is OrchestratorAction.CREATE_AIAS_REPRESENTATION
    assert not i.requires_manual_review


def test_missing_in_autocad_requires_review():
    p = coordinate_roundtrip_sync([rec("A", acad=None)])
    i = p.items[0]
    assert i.state is SyncState.MISSING_IN_AUTOCAD
    assert i.action is OrchestratorAction.REVIEW_MISSING_AUTOCAD_ENTITY
    assert i.requires_manual_review


def test_new_in_autocad_discovery_bypasses_persistent_baseline_validation():
    r = rec("A", base=None, aias=None, acad="new-acad")
    p = coordinate_roundtrip_sync([r])
    i = p.items[0]
    assert i.state is SyncState.NEW_IN_AUTOCAD
    assert i.action is OrchestratorAction.CREATE_AIAS_REPRESENTATION
    assert i.automatic_autocad_write_allowed is False
    assert i.automatic_autocad_delete_allowed is False
    assert i.requires_manual_review is False


def test_all_seven_states_consolidate_in_one_plan():
    records = [
        rec("01"),
        rec("02", aias="aias"),
        rec("03", acad="acad"),
        rec("04", aias="aias", acad="acad"),
        rec("05", aias=None),
        rec("06", acad=None),
        rec("07", base=None, aias=None, acad="new"),
    ]
    p = coordinate_roundtrip_sync(records)
    assert p.total == 7
    assert {item.state for item in p.items} == set(SyncState)
    assert sum(p.state_counts.values()) == 7
    assert p.automatic_autocad_write_count == 0
    assert p.automatic_autocad_delete_count == 0
    assert p.manual_review_count == 3
    assert p.is_safe_dry_run


def test_plan_is_deterministic_independent_of_input_order():
    records = [
        rec("03", acad="acad"),
        rec("01"),
        rec("02", aias="aias"),
    ]
    p1 = coordinate_roundtrip_sync(records)
    p2 = coordinate_roundtrip_sync(list(reversed(records)))
    assert p1.plan_fingerprint == p2.plan_fingerprint
    assert [i.autocad_handle for i in p1.items] == ["01", "02", "03"]


def test_duplicate_handle_is_primary_identity_error_even_if_id_also_duplicates():
    with pytest.raises(ValueError, match="Duplicate AutoCAD Handles"):
        coordinate_roundtrip_sync([rec("A"), rec("A", aias="different")])


def test_duplicate_aias_id_rejected_when_handles_differ():
    shared = f"autocad:{DOC}:SHARED"
    with pytest.raises(ValueError, match="Duplicate AIAS IDs"):
        coordinate_roundtrip_sync([
            rec("A", aias_id=shared),
            rec("B", aias_id=shared),
        ])


def test_cross_document_records_rejected():
    a = rec("A")
    b = AIASSyncRecord(
        document_key="other-document",
        aias_id="autocad:other-document:B",
        autocad_handle="B",
        baseline_fingerprint=BASE,
        aias_fingerprint=BASE,
        autocad_fingerprint=BASE,
    )
    with pytest.raises(ValueError, match="exactly one document"):
        coordinate_roundtrip_sync([a, b])


def test_empty_plan_rejected():
    with pytest.raises(ValueError, match="At least one"):
        coordinate_roundtrip_sync([])


def test_only_dry_run_mode_supported():
    assert RoundtripSyncCoordinator().mode is CoordinationMode.DRY_RUN


def test_new_in_autocad_pattern_is_narrow():
    # Baseline missing but AIAS already present is not NEW_IN_AUTOCAD discovery;
    # it must fall through to the persistent validator and be rejected.
    with pytest.raises(ValueError, match="baseline_fingerprint is required"):
        coordinate_roundtrip_sync([
            rec("A", base=None, aias="aias-present", acad="acad-present")
        ])


def test_no_vendor_or_write_surface_in_module():
    import aias_l3_production_bim.autocad_roundtrip_sync_coordinator as m
    source = inspect.getsource(m).lower()
    forbidden = (
        "win32com",
        "pythoncom",
        ".addline(",
        ".delete(",
        ".save(",
        "saveas",
        "sendcommand",
        "dispatch(",
        "getactiveobject",
    )
    assert all(token not in source for token in forbidden)


def test_serialized_plan_exposes_safety_counters():
    p = coordinate_roundtrip_sync([
        rec("A"),
        rec("B", aias="aias"),
        rec("C", acad=None),
    ])
    data = p.as_dict()
    assert data["mode"] == "DRY_RUN"
    assert data["automatic_autocad_write_count"] == 0
    assert data["automatic_autocad_delete_count"] == 0
    assert data["manual_review_count"] == 2
    assert data["is_safe_dry_run"] is True
    assert len(data["plan_fingerprint"]) == 64
