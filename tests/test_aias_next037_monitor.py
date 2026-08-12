from pathlib import Path
from aias_next037_monitor import CandidateMonitor
def test_monitor_does_not_mutate_missing_status(tmp_path: Path):
    result = CandidateMonitor(tmp_path / "status.json").check()
    assert result.action == "NO_MUTATION"
