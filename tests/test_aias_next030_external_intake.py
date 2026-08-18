from pathlib import Path

from aias_next030_external_intake import ExternalApprovalIntake


def test_intake_stays_pending_without_external_evidence(tmp_path: Path):
    result = ExternalApprovalIntake(tmp_path / "approval.json").inspect()
    assert result.status == "PENDING_EXTERNAL_EVIDENCE"
