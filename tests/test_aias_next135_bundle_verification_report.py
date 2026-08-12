from aias_next135_bundle_verification_report import BundleVerificationReport


def test_report_preserves_verification_and_is_local() -> None:
    result = BundleVerificationReport().generate({"valid": True, "count": 2})
    assert result["report"] == "AIAS-NEXT-135"
    assert result["verification"] == {"valid": True, "count": 2}
    assert result["external_publication"] is False
