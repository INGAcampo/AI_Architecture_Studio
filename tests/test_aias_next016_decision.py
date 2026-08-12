import json
from pathlib import Path

from aias_next016_decision import DecisionGate


def test_decision_gate_keeps_collection_open(tmp_path: Path):
    report = tmp_path / "report.json"
    report.write_text(json.dumps({"sessions": 1, "valid_records": 1, "complete": False}), encoding="utf-8")
    result = DecisionGate(report).evaluate()
    assert result.decision == "CONTINUE_COLLECTION"
