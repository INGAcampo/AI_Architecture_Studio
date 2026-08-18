from aias_next105_manifest import EvidenceManifest

def test_manifest_contains_digest(tmp_path):
    path = tmp_path / "a.txt"
    path.write_text("a", encoding="utf-8")
    result = EvidenceManifest().build([path])
    assert result["manifest"] == "AIAS-NEXT-105"
    assert len(result["entries"][0]["sha256"]) == 64
    assert result["external_publication"] is False
