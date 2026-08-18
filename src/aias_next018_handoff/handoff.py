from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HandoffManifest:
    package_id: str
    review_package: str
    required_reviewer_role: str
    approval_status: str
    sha256: str


class HandoffBuilder:
    def __init__(self, project_root: str | Path):
        self.root = Path(project_root)

    def build(self, output: str | Path | None = None) -> HandoffManifest:
        review = self.root / "engineering/aias/next017_review/REVIEW_PACKAGE.json"
        digest = hashlib.sha256(review.read_bytes()).hexdigest() if review.exists() else ""
        manifest = HandoffManifest("AIAS-NEXT-018", str(review), "independent human reviewer", "PENDING_HUMAN_REVIEW", digest)
        target = Path(output) if output else self.root / "engineering/aias/next018_handoff/HANDOFF_MANIFEST.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(manifest), ensure_ascii=False, indent=2), encoding="utf-8")
        return manifest
