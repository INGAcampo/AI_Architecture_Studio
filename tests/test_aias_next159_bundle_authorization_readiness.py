from aias_next159_bundle_authorization_readiness import BundleAuthorizationReadiness

def test_readiness_follows_gate():
    assessment = BundleAuthorizationReadiness().assess({"ready": True})
    assert assessment["status"] == "READY"
    assert assessment["external_authorization"] is False
