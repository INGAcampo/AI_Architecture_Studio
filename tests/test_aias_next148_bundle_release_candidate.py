from aias_next148_bundle_release_candidate import BundleReleaseCandidate


def test_candidate_is_not_published() -> None:
    result = BundleReleaseCandidate().create({"readiness": {"ready": True}})
    assert result["eligible"] is True
    assert result["published"] is False
