from pathlib import Path

from aias_next035_checkpoint import GovernanceCheckpoint


def test_checkpoint_holds_without_governance(tmp_path: Path):
    result = GovernanceCheckpoint(tmp_path / "governance.json", tmp_path / "external.json").evaluate()
    assert result.decision == "HOLD"
    assert result.traceable is True
