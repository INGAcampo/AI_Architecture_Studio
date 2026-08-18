from pathlib import Path
import json
import pytest

from aias_l3_production_bim.autocad_persistent_sync_state import (
    AIASSyncRecord,
    PersistentAIASSyncStateStore,
    SyncDecision,
    SyncState,
    assess_record,
    build_initial_sync_store_from_bindings,
    classify_sync_state,
)


DOC = "abc123"


def rec(base="b", aias="b", acad="b", handle="A1"):
    h = handle.upper()
    return AIASSyncRecord(
        document_key=DOC,
        aias_id=f"autocad:{DOC}:{h}",
        autocad_handle=h,
        baseline_fingerprint=base,
        aias_fingerprint=aias,
        autocad_fingerprint=acad,
    )


@pytest.mark.parametrize(
    "record,expected",
    [
        (rec(), SyncState.IN_SYNC),
        (rec(aias="a"), SyncState.AIAS_CHANGED),
        (rec(acad="c"), SyncState.AUTOCAD_CHANGED),
        (rec(aias="a", acad="c"), SyncState.BOTH_CHANGED),
        (rec(aias=None, acad="b"), SyncState.MISSING_IN_AIAS),
        (rec(aias="b", acad=None), SyncState.MISSING_IN_AUTOCAD),
    ],
)
def test_classification_matrix(record, expected):
    assert classify_sync_state(record) is expected


def test_policy_in_sync_none():
    a = assess_record(rec())
    assert a.decision is SyncDecision.NONE
    assert not a.automatic_write_allowed
    assert not a.automatic_delete_allowed


def test_policy_aias_changed_blocks_push():
    a = assess_record(rec(aias="changed"))
    assert a.state is SyncState.AIAS_CHANGED
    assert a.decision is SyncDecision.PUSH_TO_AUTOCAD_BLOCKED
    assert not a.automatic_write_allowed


def test_policy_autocad_changed_pulls():
    a = assess_record(rec(acad="changed"))
    assert a.decision is SyncDecision.PULL_FROM_AUTOCAD
    assert not a.automatic_write_allowed


def test_policy_both_changed_manual():
    a = assess_record(rec(aias="x", acad="y"))
    assert a.decision is SyncDecision.MANUAL_CONFLICT
    assert not a.automatic_delete_allowed


def test_policy_missing_autocad_never_auto_delete_recreate():
    a = assess_record(rec(acad=None))
    assert a.decision is SyncDecision.REVIEW_DELETE_OR_RECREATE
    assert not a.automatic_write_allowed
    assert not a.automatic_delete_allowed


def test_store_atomic_roundtrip(tmp_path: Path):
    p = tmp_path / "sync.json"
    s = PersistentAIASSyncStateStore(DOC)
    s.upsert(rec(handle="A1"))
    s.upsert(rec(handle="A2", aias="changed"))
    s.save_atomic(p)

    loaded = PersistentAIASSyncStateStore.load(p)
    assert len(loaded) == 2
    assert loaded.get("a1").aias_id == f"autocad:{DOC}:A1"
    assert loaded.summary()[SyncState.AIAS_CHANGED.value] == 1


def test_tamper_rejected(tmp_path: Path):
    p = tmp_path / "sync.json"
    s = PersistentAIASSyncStateStore(DOC)
    s.upsert(rec())
    s.save_atomic(p)

    payload = json.loads(p.read_text())
    payload["records"][0]["aias_fingerprint"] = "tampered"
    p.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="SHA-256"):
        PersistentAIASSyncStateStore.load(p)


def test_initial_store_from_bindings_is_clean():
    payload = {
        "document_key": DOC,
        "records": [
            {
                "document_key": DOC,
                "aias_id": f"autocad:{DOC}:A1",
                "autocad_handle": "A1",
                "fingerprint": "f1",
            },
            {
                "document_key": DOC,
                "aias_id": f"autocad:{DOC}:A2",
                "autocad_handle": "A2",
                "fingerprint": "f2",
            },
        ],
    }
    store = build_initial_sync_store_from_bindings(payload)
    assert len(store) == 2
    assert store.summary()[SyncState.IN_SYNC.value] == 2


def test_cross_document_record_rejected():
    store = PersistentAIASSyncStateStore(DOC)
    with pytest.raises(ValueError, match="document_key"):
        store.upsert(
            AIASSyncRecord(
                document_key="other",
                aias_id="autocad:other:A1",
                autocad_handle="A1",
                baseline_fingerprint="f",
                aias_fingerprint="f",
                autocad_fingerprint="f",
            )
        )


def test_no_vendor_or_write_surface():
    s = PersistentAIASSyncStateStore(DOC)
    forbidden = {
        "Save", "SaveAs", "SendCommand", "Dispatch", "CreateObject",
        "save", "save_as", "send_command", "dispatch", "create_object",
        "delete_entity", "update_entity", "create_entity",
    }
    assert forbidden.isdisjoint(set(dir(s)))
