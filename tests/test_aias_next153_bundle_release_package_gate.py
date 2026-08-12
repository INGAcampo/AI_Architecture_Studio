from aias_next153_bundle_release_package_gate import BundleReleasePackageGate


def test_gate_requires_valid_package_report() -> None:
    gate = BundleReleasePackageGate()
    assert gate.evaluate({"verification": {"valid": True}})["ready"] is True
    assert gate.evaluate({"verification": {"valid": False}})["ready"] is False
