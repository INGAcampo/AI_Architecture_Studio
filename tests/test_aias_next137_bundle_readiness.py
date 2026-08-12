from aias_next137_bundle_readiness import BundleReadiness


def test_readiness_follows_gate() -> None:
    result = BundleReadiness().assess({"ready": True})
    assert result == {
        "assessment": "AIAS-NEXT-137",
        "ready": True,
        "status": "READY",
        "external_release": False,
    }
