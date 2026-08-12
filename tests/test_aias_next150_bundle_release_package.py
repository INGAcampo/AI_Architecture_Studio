from aias_next150_bundle_release_package import BundleReleasePackage


def test_package_assembles_local_artifacts() -> None:
    result = BundleReleasePackage().assemble([{"path": "manifest.json"}])
    assert result["package"] == "AIAS-NEXT-150"
    assert result["count"] == 1
    assert result["published"] is False
