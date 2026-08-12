from aias_next146_bundle_release_readiness import BundleReleaseReadiness


def test_readiness_requires_valid_report() -> None:
    gate = BundleReleaseReadiness()
    assert gate.evaluate({"verification": {"valid": True}})["status"] == "READY"
    assert gate.evaluate({"verification": {"valid": False}})["status"] == "HOLD"
