from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class FinalReviewPackage:
    package_id: str
    status: str
    checklist: tuple[str, ...]
    release_approved: bool


class FinalReviewBuilder:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def build(self, output: str | Path | None = None) -> FinalReviewPackage:
        package = FinalReviewPackage("AIAS-NEXT-036", "PENDING_REVIEW", ("artifact integrity", "external gates", "production approval", "independent decision"), False)
        target = Path(output) if output else self.root / "engineering/aias/next036_review/FINAL_REVIEW_PACKAGE.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(package), ensure_ascii=False, indent=2), encoding="utf-8")
        return package
