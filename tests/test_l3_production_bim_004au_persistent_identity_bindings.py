from pathlib import Path
import json
import pytest

from aias_l3_production_bim.autocad_persistent_identity_bindings import (
    IdentityBinding,
    PersistentIdentityBindingStore,
    bindings_from_certified_baseline,
)


DOC = "abc123"


def b(handle="A1", fp="fp1"):
    handle = handle.upper()
    return IdentityBinding(
        document_key=DOC,
        aias_id=f"autocad:{DOC}:{handle}",
        autocad_handle=handle,
        fingerprint=fp,
        object_name="AcDbLine",
        layer="vista",
    )


def test_bind_and_lookup_bidirectional():
    s = PersistentIdentityBindingStore(DOC)
    x = b()
    s.bind(x)
    assert s.get_by_handle("a1").aias_id == x.aias_id
    assert s.get_by_aias_id(x.aias_id).autocad_handle == "A1"


def test_rejects_unstable_aias_id():
    s = PersistentIdentityBindingStore(DOC)
    with pytest.raises(ValueError, match="Unstable AIAS ID"):
        s.bind(IdentityBinding(DOC, "wrong", "A1", "fp"))


def test_rejects_cross_document_binding():
    s = PersistentIdentityBindingStore(DOC)
    with pytest.raises(ValueError, match="document_key"):
        s.bind(IdentityBinding("other", "autocad:other:A1", "A1", "fp"))


def test_unbind_removes_reverse_index():
    s = PersistentIdentityBindingStore(DOC)
    x = b()
    s.bind(x)
    assert s.unbind_handle("A1") == x
    assert s.get_by_handle("A1") is None
    assert s.get_by_aias_id(x.aias_id) is None


def test_reconcile_clean():
    s = PersistentIdentityBindingStore(DOC)
    s.bind(b("A1", "f1"))
    s.bind(b("A2", "f2"))
    r = s.reconcile([b("A1", "f1"), b("A2", "f2")])
    assert r.clean
    assert r.in_sync == ("A1", "A2")


def test_reconcile_detects_all_drift_classes():
    s = PersistentIdentityBindingStore(DOC)
    s.bind(b("A1", "old"))
    s.bind(b("A3", "f3"))
    r = s.reconcile([b("A1", "new"), b("A2", "f2")])
    assert not r.clean
    assert r.fingerprint_mismatches == ("A1",)
    assert r.missing_in_store == ("A2",)
    assert r.missing_in_source == ("A3",)


def test_atomic_roundtrip(tmp_path: Path):
    p = tmp_path / "bindings.json"
    s = PersistentIdentityBindingStore(DOC)
    s.bind(b("A1", "f1"))
    s.bind(b("A2", "f2"))
    s.save_atomic(p)

    loaded = PersistentIdentityBindingStore.load(p)
    assert len(loaded) == 2
    assert loaded.reconcile(s.bindings()).clean


def test_tampered_payload_rejected(tmp_path: Path):
    p = tmp_path / "bindings.json"
    s = PersistentIdentityBindingStore(DOC)
    s.bind(b("A1", "f1"))
    s.save_atomic(p)

    payload = json.loads(p.read_text())
    payload["records"][0]["fingerprint"] = "tampered"
    p.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="SHA-256"):
        PersistentIdentityBindingStore.load(p)


def test_bindings_from_certified_baseline():
    payload = {
        "document_key": DOC,
        "records": [
            {
                "autocad_handle": "A1",
                "aias_id": f"autocad:{DOC}:A1",
                "fingerprint": "f1",
                "mapped": {"object_name": "AcDbLine", "layer": "vista"},
            }
        ],
    }
    result = bindings_from_certified_baseline(payload)
    assert len(result) == 1
    assert result[0].object_name == "AcDbLine"
    assert result[0].layer == "vista"


def test_no_vendor_or_persistence_surface():
    s = PersistentIdentityBindingStore(DOC)
    forbidden = {
        "Save", "SaveAs", "SendCommand", "Dispatch", "CreateObject",
        "save", "save_as", "send_command", "dispatch", "create_object",
    }
    assert forbidden.isdisjoint(set(dir(s)))
