from aias_next096_release import ReleasePackage

def test_release_package_is_reproducible_and_private():
    result = ReleasePackage().build(["dashboard.json", "manifest.json", "dashboard.json"])
    assert result["artifacts"] == ["dashboard.json", "manifest.json"]
    assert result["reproducible"] is True
    assert result["published_externally"] is False
