import json
from pathlib import Path

from aias_next025_audit import RoadmapIntegrityAudit


def test_audit_preserves_deferred_items(tmp_path: Path):
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"current": "A", "next": "B", "backlog": ["DEFERRED: C"]}), encoding="utf-8")
    result = RoadmapIntegrityAudit(plan).run()
    assert result.valid is True
    assert result.deferred_items == ("DEFERRED: C",)
