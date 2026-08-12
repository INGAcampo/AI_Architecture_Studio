from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MaturityReport:
    reference_capability_level: int | None
    audited_organizational_level: int | None
    campaign_status: str
    evidence_warning: str


class MaturityReconciler:
    def __init__(self, dashboard_snapshot: str | Path):
        self.path = Path(dashboard_snapshot)

    def reconcile(self, output: str | Path | None = None) -> MaturityReport:
        if not self.path.exists():
            report = MaturityReport(None, None, "UNKNOWN", "Dashboard snapshot absent")
        else:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            maturity = data.get("maturity", data)
            report = MaturityReport(maturity.get("reference_capability_level"), maturity.get("audited_organizational_level"), maturity.get("campaign_status", "UNKNOWN"), maturity.get("warning", ""))
        if output:
            destination = Path(output)
        else:
            destination = self.path.parent / "MATURITY_RECONCILIATION.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")
        return report
