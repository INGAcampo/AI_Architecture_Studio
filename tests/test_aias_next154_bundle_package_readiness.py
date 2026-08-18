from aias_next154_bundle_package_readiness import BundlePackageReadiness


def test_readiness_follows_package_gate() -> None:
    readiness = BundlePackageReadiness()
    assert readiness.assess({"ready": True})["status"] == "READY"
    assert readiness.assess({"ready": False})["status"] == "HOLD"
