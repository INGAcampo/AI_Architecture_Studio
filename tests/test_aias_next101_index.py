from aias_next101_index import ArtifactIndex

def test_index_is_sorted_and_unique():
    result = ArtifactIndex().build(["b", "a", "a"])
    assert result["artifacts"] == ["a", "b"]
    assert result["count"] == 2
    assert result["external_publication"] is False
