from aias_next147_bundle_release_readiness_report import BundleReleaseReadinessReport


def test_readiness_report_preserves_state() -> None:
    result = BundleReleaseReadinessReport().generate({"ready": True, "status": "READY"})
    assert result["report"] == "AIAS-NEXT-147"
    assert result["readiness"]["status"] == "READY"
    assert result["external_approval"] is False
