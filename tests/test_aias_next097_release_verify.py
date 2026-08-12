from aias_next097_release_verify import ReleaseVerifier

def test_verifier_detects_duplicate_artifacts():
    result = ReleaseVerifier().verify(["a", "a"])
    assert result["unique"] is False
    assert result["published_externally"] is False
