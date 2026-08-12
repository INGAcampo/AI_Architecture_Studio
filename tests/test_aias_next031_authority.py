from pathlib import Path

from aias_next031_authority import AuthorityWorkflow


def test_authority_workflow_starts_pending(tmp_path: Path):
    result = AuthorityWorkflow(tmp_path / "evidence.json").evaluate()
    assert result.stage == "INTAKE_PENDING"
    assert result.approval_granted is False
