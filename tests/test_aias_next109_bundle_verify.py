from aias_next109_bundle_verify import BundleVerifier

def test_bundle_verifier_detects_duplicates():
    result = BundleVerifier().verify(["a", "a"])
    assert result["unique"] is False
    assert result["valid"] is False
    assert result["external_validity"] is False
