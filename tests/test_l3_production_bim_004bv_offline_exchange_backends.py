from __future__ import annotations

import json
from pathlib import Path

import pytest

from aias_l3_production_bim.offline_exchange_backends import (
    Geo5OfflineExchangeBackend,
    OfflineExchangeTarget,
    SketchUpOfflineExchangeBackend,
)


def make_file(tmp_path: Path, name: str, content: bytes = b"AIAS") -> Path:
    p = tmp_path / name
    p.write_bytes(content)
    return p


def test_sketchup_backend_identity():
    b = SketchUpOfflineExchangeBackend()
    assert b.target is OfflineExchangeTarget.SKETCHUP
    assert ".skp" in b.forbidden_proprietary_extensions


def test_geo5_backend_identity():
    b = Geo5OfflineExchangeBackend()
    assert b.target is OfflineExchangeTarget.GEO5
    assert b.forbidden_proprietary_extensions


def test_sketchup_neutral_bundle_stages_and_verifies(tmp_path):
    src = make_file(tmp_path, "model.ifc", b"ifc-data")
    out = tmp_path / "bundle"
    b = SketchUpOfflineExchangeBackend()
    bundle = b.stage_bundle([src], out)
    assert bundle.artifact_count == 1
    assert bundle.vendor_runtime_verified is False
    assert bundle.proprietary_format_written is False
    assert bundle.launch_performed is False
    assert b.verify_bundle(out) is True


def test_geo5_neutral_bundle_stages_and_verifies(tmp_path):
    src = make_file(tmp_path, "terrain.dxf", b"dxf-data")
    out = tmp_path / "bundle"
    b = Geo5OfflineExchangeBackend()
    bundle = b.stage_bundle([src], out)
    assert bundle.artifact_count == 1
    assert b.verify_bundle(out) is True


def test_sketchup_proprietary_skp_rejected(tmp_path):
    src = make_file(tmp_path, "model.skp")
    with pytest.raises(ValueError, match="Proprietary target format"):
        SketchUpOfflineExchangeBackend().stage_bundle([src], tmp_path / "bundle")


def test_geo5_proprietary_format_rejected(tmp_path):
    src = make_file(tmp_path, "project.gmk")
    with pytest.raises(ValueError, match="Proprietary target format"):
        Geo5OfflineExchangeBackend().stage_bundle([src], tmp_path / "bundle")


def test_unknown_extension_rejected(tmp_path):
    src = make_file(tmp_path, "payload.bin")
    with pytest.raises(ValueError, match="Unsupported neutral"):
        SketchUpOfflineExchangeBackend().stage_bundle([src], tmp_path / "bundle")


def test_missing_source_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        Geo5OfflineExchangeBackend().stage_bundle(
            [tmp_path / "missing.dxf"],
            tmp_path / "bundle",
        )


def test_empty_bundle_rejected(tmp_path):
    with pytest.raises(ValueError, match="At least one"):
        SketchUpOfflineExchangeBackend().stage_bundle([], tmp_path / "bundle")


def test_duplicate_names_rejected(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    p1 = make_file(a, "same.dxf", b"1")
    p2 = make_file(b, "same.dxf", b"2")
    with pytest.raises(ValueError, match="Duplicate staged file names"):
        Geo5OfflineExchangeBackend().stage_bundle([p1, p2], tmp_path / "bundle")


def test_manifest_safety_flags_are_explicit(tmp_path):
    src = make_file(tmp_path, "model.obj", b"obj")
    out = tmp_path / "bundle"
    SketchUpOfflineExchangeBackend().stage_bundle([src], out)
    data = json.loads((out / "AIAS_EXCHANGE_MANIFEST.json").read_text())
    assert data["vendor_runtime_verified"] is False
    assert data["proprietary_format_written"] is False
    assert data["launch_performed"] is False
    assert data["compatibility_certified"] is False


def test_tampering_detected(tmp_path):
    src = make_file(tmp_path, "terrain.csv", b"x,y\n1,2\n")
    out = tmp_path / "bundle"
    b = Geo5OfflineExchangeBackend()
    b.stage_bundle([src], out)
    (out / "terrain.csv").write_bytes(b"tampered")
    assert b.verify_bundle(out) is False


def test_manifest_tampering_detected(tmp_path):
    src = make_file(tmp_path, "model.dae", b"dae")
    out = tmp_path / "bundle"
    b = SketchUpOfflineExchangeBackend()
    b.stage_bundle([src], out)
    manifest = out / "AIAS_EXCHANGE_MANIFEST.json"
    data = json.loads(manifest.read_text())
    data["vendor_runtime_verified"] = True
    manifest.write_text(json.dumps(data))
    assert b.verify_bundle(out) is False


def test_existing_manifest_requires_explicit_overwrite(tmp_path):
    src = make_file(tmp_path, "terrain.xml", b"<x/>")
    out = tmp_path / "bundle"
    b = Geo5OfflineExchangeBackend()
    b.stage_bundle([src], out)
    with pytest.raises(FileExistsError):
        b.stage_bundle([src], out)


def test_overwrite_replaces_existing_bundle_artifact(tmp_path):
    src = make_file(tmp_path, "terrain.xml", b"<x/>")
    out = tmp_path / "bundle"
    b = Geo5OfflineExchangeBackend()
    b.stage_bundle([src], out)
    src.write_bytes(b"<y/>")
    b.stage_bundle([src], out, overwrite=True)
    assert (out / "terrain.xml").read_bytes() == b"<y/>"
    assert b.verify_bundle(out) is True


def test_multiple_files_sorted_deterministically(tmp_path):
    a = make_file(tmp_path, "z.dxf", b"z")
    bfile = make_file(tmp_path, "a.ifc", b"a")
    out = tmp_path / "bundle"
    bundle = SketchUpOfflineExchangeBackend().stage_bundle([a, bfile], out)
    assert [x.staged_name for x in bundle.artifacts] == ["a.ifc", "z.dxf"]


def test_bundle_never_claims_vendor_runtime(tmp_path):
    src = make_file(tmp_path, "terrain.txt", b"safe")
    bundle = Geo5OfflineExchangeBackend().stage_bundle([src], tmp_path / "bundle")
    payload = bundle.as_dict()
    assert payload["vendor_runtime_verified"] is False
    assert payload["proprietary_format_written"] is False
    assert payload["launch_performed"] is False
