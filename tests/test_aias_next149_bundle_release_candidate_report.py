from aias_next149_bundle_release_candidate_report import BundleReleaseCandidateReport


def test_candidate_report_is_local() -> None:
    result = BundleReleaseCandidateReport().generate({"eligible": True})
    assert result["report"] == "AIAS-NEXT-149"
    assert result["candidate"]["eligible"] is True
    assert result["published"] is False
