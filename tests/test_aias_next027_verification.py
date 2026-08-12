from pathlib import Path

from aias_next027_verification import CandidateVerifier


def test_verification_never_grants_production_approval(tmp_path: Path):
    report = CandidateVerifier(tmp_path).verify()
    assert report.production_approval is False
    assert report.local_verification is False
