from pathlib import Path

from shadow_test_factory.manifest import build_manifest, sha256_file


def test_sha256_file_is_deterministic(tmp_path):
    path = tmp_path / "a.txt"
    path.write_text("AIAS", encoding="ascii")

    first = sha256_file(path)
    second = sha256_file(path)

    assert first == second
    assert len(first) == 64


def test_manifest_is_sorted_and_contains_hashes(tmp_path):
    (tmp_path / "b.txt").write_text("B", encoding="ascii")
    (tmp_path / "a.txt").write_text("A", encoding="ascii")

    manifest = build_manifest(tmp_path)

    assert [item["path"] for item in manifest] == ["a.txt", "b.txt"]
    assert all(len(item["sha256"]) == 64 for item in manifest)
    assert all(item["bytes"] == 1 for item in manifest)
