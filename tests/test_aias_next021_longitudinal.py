from pathlib import Path

from aias_next021_longitudinal import LongitudinalMonitor


def test_longitudinal_monitor_does_not_invent_observation_time(tmp_path: Path):
    result = LongitudinalMonitor(tmp_path / "missing.jsonl").measure()
    assert result.observation_days == 0.0
    assert result.sufficient_for_365_days is False
