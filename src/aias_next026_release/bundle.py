from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReleaseEvidenceBundle:
    status: str
    artifacts: tuple[dict[str, str], ...]
    external_gates_pending: bool


class BundleBuilder:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def build(self, output: str | Path | None = None) -> ReleaseEvidenceBundle:
        candidates = [self.root / "ACKC/MASTER_CONTEXT.json", self.root / "aias_productivity_dashboard_outputs_20260812/AIAS_PRODUCTIVITY_SNAPSHOT.json"]
        candidates.extend(sorted(self.root.glob("AIAS_NEXT*_INSTALLER/checksums.sha256")))
        artifacts = tuple({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in candidates if path.exists())
        bundle = ReleaseEvidenceBundle("RELEASE_CANDIDATE_EVIDENCE_ONLY", artifacts, True)
        target = Path(output) if output else self.root / "engineering/aias/next026_release/RELEASE_EVIDENCE_BUNDLE.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(bundle), ensure_ascii=False, indent=2), encoding="utf-8")
        return bundle
