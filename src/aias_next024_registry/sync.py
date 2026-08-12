from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SyncResult:
    authority_count: int
    evidence_count: int
    matched_ids: tuple[str, ...]
    unmatched_authorities: tuple[str, ...]
    status: str


class RegistrySynchronizer:
    def __init__(self, authority_path: str | Path, evidence_path: str | Path):
        self.authority_path = Path(authority_path)
        self.evidence_path = Path(evidence_path)

    def synchronize(self) -> SyncResult:
        authorities = self._entries(self.authority_path)
        evidence = self._entries(self.evidence_path)
        authority_ids = {str(item.get("id")) for item in authorities if item.get("id") is not None}
        evidence_ids = {str(item.get("authority_id", item.get("id"))) for item in evidence if item.get("authority_id", item.get("id")) is not None}
        matched = tuple(sorted(authority_ids & evidence_ids))
        unmatched = tuple(sorted(authority_ids - evidence_ids))
        return SyncResult(len(authorities), len(evidence), matched, unmatched, "ALIGNED" if not unmatched else "EVIDENCE_PENDING")

    @staticmethod
    def _entries(path: Path) -> list[dict]:
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data.get("entries", [])
