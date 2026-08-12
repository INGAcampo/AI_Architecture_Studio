from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExternalStatusReport:
    gates: tuple[dict[str, str], ...]
    all_approved: bool
    release_blocked: bool


class ExternalStatusBuilder:
    def __init__(self, registry_path: str | Path):
        self.path = Path(registry_path)

    def build(self, output: str | Path | None = None) -> ExternalStatusReport:
        if not self.path.exists():
            gates = ({"id": "REGISTRY", "status": "PENDING"},)
        else:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            gates = tuple({"id": str(item.get("id", "UNKNOWN")), "status": str(item.get("status", "PENDING"))} for item in data.get("entries", data if isinstance(data, list) else []))
        approved = bool(gates) and all(item["status"] == "APPROVED" for item in gates)
        report = ExternalStatusReport(gates, approved, not approved)
        if output:
            destination = Path(output)
        else:
            destination = self.path.parent / "EXTERNAL_STATUS_REPORT.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
        return report
