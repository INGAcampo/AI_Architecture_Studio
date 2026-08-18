"""Read-only monitor for an approved historical publication artifact."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any

class PublicationMonitor:
    """Detect presence and SHA-256 changes without mutating the artifact."""
    def __init__(self, publication_path: str | Path):
        self.publication_path = Path(publication_path)
    def check(self, previous_sha256: str | None = None) -> dict[str, Any]:
        if not self.publication_path.exists():
            return {"status": "NO_PUBLICATION", "observed": False, "changed": False}
        digest = hashlib.sha256(self.publication_path.read_bytes()).hexdigest()
        return {"status": "PUBLICATION_OBSERVED", "observed": True, "sha256": digest, "changed": previous_sha256 is not None and digest != previous_sha256}
