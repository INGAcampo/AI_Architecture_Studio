from pathlib import Path

from aias_next020_closure import ClosureGate


def test_closure_stays_open_without_artifacts(tmp_path: Path):
    result = ClosureGate(tmp_path / "review.json", tmp_path / "handoff.json").evaluate()
    assert result.status == "OPEN_COLLECTION"
