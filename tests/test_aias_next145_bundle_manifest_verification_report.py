from aias_next145_bundle_manifest_verification_report import BundleManifestVerificationReport


def test_report_preserves_manifest_verification() -> None:
    result = BundleManifestVerificationReport().generate({"valid": True, "count": 1})
    assert result["report"] == "AIAS-NEXT-145"
    assert result["verification"] == {"valid": True, "count": 1}
    assert result["local_only"] is True
