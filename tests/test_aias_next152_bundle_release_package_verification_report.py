from aias_next152_bundle_release_package_verification_report import BundleReleasePackageVerificationReport


def test_report_preserves_package_verification() -> None:
    result = BundleReleasePackageVerificationReport().generate({"valid": True, "count": 1})
    assert result["report"] == "AIAS-NEXT-152"
    assert result["verification"]["valid"] is True
    assert result["local_only"] is True
