import json
from pathlib import Path
from aias_continuity_watch import ContinuityWatch
ROOT=Path(__file__).resolve().parents[1]
def test_watch_holds_when_next_task_requires_authority():
    decision=ContinuityWatch().inspect(ROOT)
    assert decision.next_task and decision.action in {"CONTINUE_SAFE","HOLD_FOR_AUTHORITY","STOP"}
def test_watch_spec_prohibits_mutation():
    spec=json.loads((ROOT/"engineering/aias/continuity_watch/AIAS_NEXT_010_SPEC.json").read_text(encoding="utf-8"))
    assert "watcher does not mutate source" in spec["invariants"]
