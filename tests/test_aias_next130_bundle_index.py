from aias_next130_bundle_index import BundleArtifactIndex

def test_bundle_index_is_sorted_unique():
    result = BundleArtifactIndex().build(["report", "index", "index"])
    assert result["artifacts"] == ["index", "report"]
    assert result["count"] == 2
    assert result["external_publication"] is False
