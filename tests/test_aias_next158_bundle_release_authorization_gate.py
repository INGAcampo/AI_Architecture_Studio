from aias_next158_bundle_release_authorization_gate import BundleReleaseAuthorizationGate

def test_gate_is_internal():
    gate = BundleReleaseAuthorizationGate()
    assert gate.evaluate({"authorization": {"internally_authorized": True}})["ready"] is True
    assert gate.evaluate({"authorization": {"internally_authorized": False}})["ready"] is False
