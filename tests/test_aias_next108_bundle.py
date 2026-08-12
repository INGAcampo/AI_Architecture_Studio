from aias_next108_bundle import EvidenceBundle

def test_bundle_is_sorted_and_local():
    result = EvidenceBundle().build(["z", "a", "a"])
    assert result["reports"] == ["a", "z"]
    assert result["count"] == 2
    assert result["external_publication"] is False
