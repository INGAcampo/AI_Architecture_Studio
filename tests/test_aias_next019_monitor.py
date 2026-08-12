import json
from pathlib import Path

from aias_next019_monitor import ReviewMonitor


def test_monitor_does_not_infer_approval(tmp_path: Path):
    handoff = tmp_path / "handoff.json"
    handoff.write_text(json.dumps({"approval_status": "PENDING_HUMAN_REVIEW"}), encoding="utf-8")
    result = ReviewMonitor(handoff).check()
    assert result.status == "PENDING_HUMAN_REVIEW"
    assert result.approval_evidence_present is False
