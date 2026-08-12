import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_aias_next_strategy_has_governed_order_and_safety_gates():
    strategy = json.loads((ROOT / "engineering/aias/roadmap/AIAS_NEXT_STRATEGY.json").read_text(encoding="utf-8"))
    assert strategy["status"] == "ACTIVE_GOVERNED_STRATEGY"
    assert [phase["id"] for phase in strategy["phases"][:4]] == ["G0", "G1", "G2", "G3"]
    assert "EXP-COMMS-001" in strategy["deferred"]
    assert "No normative compliance" in strategy["principles"][-1]


def test_golden_baseline_is_not_falsely_declared_frozen():
    baseline = json.loads((ROOT / "engineering/aias/roadmap/AIAS_CURRENT_GOLDEN_BASELINE_CANDIDATE.json").read_text(encoding="utf-8"))
    assert baseline["status"] == "CANDIDATE_NOT_FROZEN"
    assert len(baseline["required_freeze_gates"]) >= 5
