from aias_next155_bundle_package_readiness_report import BundlePackageReadinessReport


def test_readiness_report_is_local() -> None:
    result = BundlePackageReadinessReport().generate({"status": "READY"})
    assert result["report"] == "AIAS-NEXT-155"
    assert result["readiness"]["status"] == "READY"
    assert result["external_approval"] is False
