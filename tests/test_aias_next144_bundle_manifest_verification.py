from aias_next144_bundle_manifest_verification import BundleManifestVerification


def test_manifest_verification_accepts_complete_entries() -> None:
    result = BundleManifestVerification().verify([{"path": "a", "sha256": "abc"}])
    assert result["valid"] is True


def test_manifest_verification_rejects_missing_hash() -> None:
    assert BundleManifestVerification().verify([{"path": "a", "sha256": ""}])["valid"] is False
