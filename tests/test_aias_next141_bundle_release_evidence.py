from aias_next141_bundle_release_evidence import BundleReleaseEvidence


def test_consolidate_preserves_local_reports() -> None:
    result = BundleReleaseEvidence().consolidate([{"ready": True}])
    assert result["evidence"] == "AIAS-NEXT-141"
    assert result["reports"] == [{"ready": True}]
    assert result["external_release"] is False
