from aias_next151_bundle_release_package_verification import BundleReleasePackageVerification


def test_package_verification_checks_count() -> None:
    verifier = BundleReleasePackageVerification()
    assert verifier.verify({"artifacts": [{"path": "a"}], "count": 1})["valid"] is True
    assert verifier.verify({"artifacts": [{"path": "a"}], "count": 2})["valid"] is False
