from aias_next138_bundle_artifact_index import BundleArtifactIndex


def test_index_is_sorted_and_ordinal() -> None:
    result = BundleArtifactIndex().build(["z.json", "a.json", "a.json"])
    assert result["artifacts"] == [
        {"ordinal": 1, "path": "a.json"},
        {"ordinal": 2, "path": "z.json"},
    ]
    assert result["local_only"] is True
