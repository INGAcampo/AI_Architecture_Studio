from aias_next131_bundle_index_integrity import BundleIndexIntegrity

def test_bundle_index_integrity_accepts_sorted_unique():
    result = BundleIndexIntegrity().verify({"artifacts": ["a", "b"]})
    assert result["valid"] is True
    assert len(result["sha256"]) == 64
    assert result["external_validity"] is False
