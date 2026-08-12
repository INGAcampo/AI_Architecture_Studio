from aias_next134_bundle_verification import BundleVerification


def test_verification_accepts_unique_non_empty_reports() -> None:
    result = BundleVerification().verify(["index", "integrity"])
    assert result["valid"] is True
    assert result["unique"] is True
    assert result["non_empty"] is True


def test_verification_rejects_duplicates_and_empty_values() -> None:
    result = BundleVerification().verify(["index", "index", " "])
    assert result["valid"] is False
