from aias_next140_bundle_index_integrity_report import BundleIndexIntegrityReport


def test_report_preserves_integrity() -> None:
    result = BundleIndexIntegrityReport().generate({"valid": True, "count": 2})
    assert result == {
        "report": "AIAS-NEXT-140",
        "integrity": {"valid": True, "count": 2},
        "local_only": True,
    }
