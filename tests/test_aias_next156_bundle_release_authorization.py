from aias_next156_bundle_release_authorization import BundleReleaseAuthorization


def test_authorization_is_internal_only() -> None:
    result = BundleReleaseAuthorization().record({"readiness": {"ready": True}})
    assert result["internally_authorized"] is True
    assert result["external_authorization"] is False
