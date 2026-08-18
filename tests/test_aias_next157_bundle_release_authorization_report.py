from aias_next157_bundle_release_authorization_report import BundleReleaseAuthorizationReport


def test_authorization_report_is_internal() -> None:
    result = BundleReleaseAuthorizationReport().generate({"internally_authorized": True})
    assert result["report"] == "AIAS-NEXT-157"
    assert result["authorization"]["internally_authorized"] is True
    assert result["external_authority"] is False
