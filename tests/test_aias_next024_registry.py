import json
from pathlib import Path

from aias_next024_registry import RegistrySynchronizer


def test_registry_sync_reports_pending_evidence(tmp_path: Path):
    authority = tmp_path / "authority.json"
    evidence = tmp_path / "evidence.json"
    authority.write_text(json.dumps({"entries": [{"id": "EXT-1"}]}), encoding="utf-8")
    evidence.write_text(json.dumps({"entries": []}), encoding="utf-8")
    result = RegistrySynchronizer(authority, evidence).synchronize()
    assert result.status == "EVIDENCE_PENDING"
    assert result.unmatched_authorities == ("EXT-1",)
