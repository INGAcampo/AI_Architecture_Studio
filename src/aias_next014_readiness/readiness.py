from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class ReadinessReport:
    ready: bool
    records_path: str
    checklist: tuple[str, ...]


class CampaignReadiness:
    def __init__(self, project_root: str | Path):
        self.root = Path(project_root)

    def inspect(self) -> ReadinessReport:
        spec = self.root / "engineering/aias/usability_campaign/AIAS_W2_07_SPEC.json"
        template = self.root / "engineering/aias/usability_campaign/SESSION_TEMPLATE.json"
        records = self.root / "engineering/aias/usability_campaign/SESSION_RECORDS.jsonl"
        checks = []
        if spec.exists() and template.exists():
            checks.append("protocol and template present")
        else:
            checks.append("protocol or template missing")
        checks.append("records file present" if records.exists() else "records file awaiting first real session")
        return ReadinessReport(spec.exists() and template.exists(), str(records), tuple(checks))
