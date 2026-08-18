from aias_next094_integrity import IntegrityVerifier
import hashlib

def test_integrity_matches_digest(tmp_path):
    path = tmp_path / "evidence.json"
    path.write_text("{}", encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = IntegrityVerifier().verify(path, digest)
    assert result["match"] is True
    assert result["certification"] is False
