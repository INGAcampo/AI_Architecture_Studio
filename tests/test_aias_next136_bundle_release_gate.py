from aias_next136_bundle_release_gate import BundleReleaseGate


def test_gate_opens_only_for_valid_verification() -> None:
    gate = BundleReleaseGate()
    assert gate.evaluate({"valid": True})["ready"] is True
    assert gate.evaluate({"valid": False})["ready"] is False
    assert gate.evaluate({"valid": True})["external_approval"] is False
