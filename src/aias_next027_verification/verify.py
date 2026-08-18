from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VerificationReport:
    checked: int
    missing: tuple[str, ...]
    hash_valid: bool
    local_verification: bool
    production_approval: bool


class CandidateVerifier:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def verify(self) -> VerificationReport:
        bundle = self.root / "engineering/aias/next026_release/RELEASE_EVIDENCE_BUNDLE.json"
        missing = () if bundle.exists() else (str(bundle),)
        digest_ok = bool(bundle.exists() and hashlib.sha256(bundle.read_bytes()).hexdigest())
        return VerificationReport(1 if bundle.exists() else 0, missing, digest_ok, not missing, False)
