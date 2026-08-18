from aias_next106_manifest_verify import ManifestVerifier
import hashlib

def test_manifest_verifier_matches_file(tmp_path):
    path = tmp_path / "a.txt"
    path.write_text("a", encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = ManifestVerifier().verify([{"path": str(path), "sha256": digest}])
    assert result["valid"] is True
    assert result["external_validity"] is False
