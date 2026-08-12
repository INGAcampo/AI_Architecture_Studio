import json
from pathlib import Path

from aias_next012_selection import MacrodeliverySelector


def test_selects_declared_next_and_preserves_deferred_items(tmp_path: Path):
    root = tmp_path
    plan = root / "engineering/aias/master"
    plan.mkdir(parents=True)
    (plan / "AIAS_MASTER_DEVELOPMENT_PLAN.json").write_text(json.dumps({"next": "AIAS-NEXT-012 X", "backlog": ["DEFERRED: EXP-COMMS-001"]}), encoding="utf-8")
    result = MacrodeliverySelector(root).select()
    assert result.selected == "AIAS-NEXT-012 X"
    assert result.deferred == ("EXP-COMMS-001",)
