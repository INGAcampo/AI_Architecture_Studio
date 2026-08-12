from aias_next142_bundle_release_evidence_report import BundleReleaseEvidenceReport


def test_report_preserves_evidence() -> None:
    result = BundleReleaseEvidenceReport().generate({"count": 1, "external_release": False})
    assert result["report"] == "AIAS-NEXT-142"
    assert result["evidence"]["count"] == 1
    assert result["external_authority"] is False
