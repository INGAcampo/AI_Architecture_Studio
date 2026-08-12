from aias_next143_bundle_release_manifest import BundleReleaseManifest


def test_manifest_is_sorted_and_local() -> None:
    result = BundleReleaseManifest().build([
        {"path": "z", "sha256": "2"},
        {"path": "a", "sha256": "1"},
    ])
    assert [item["path"] for item in result["artifacts"]] == ["a", "z"]
    assert result["local_only"] is True
