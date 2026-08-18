from pathlib import Path

from aias_next028_readiness import ReleaseReadinessGate


def test_readiness_holds_without_artifacts(tmp_path: Path):
    result = ReleaseReadinessGate(tmp_path / "verify.json", tmp_path / "bundle.json").evaluate()
    assert result.decision == "HOLD_CANDIDATE"
