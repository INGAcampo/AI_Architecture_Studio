"""File-level SHA-256 inventory and canonical revision-manifest generation."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .models import RevisionManifest


def sha256(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of an artifact's exact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_revision_manifest(source: Path, package_id: str, revision: str, source_package: str) -> RevisionManifest:
    """Inventory non-release source files and hash the canonical revision payload."""
    files = [
        {"path": path.relative_to(source).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in sorted(source.rglob("*"))
        if path.is_file() and "release" not in path.parts
    ]
    canonical = json.dumps({"package_id": package_id, "revision": revision, "source_package": source_package, "files": files}, sort_keys=True, separators=(",", ":"))
    return RevisionManifest(package_id, revision, source_package, datetime.now(timezone.utc).isoformat(), files, hashlib.sha256(canonical.encode()).hexdigest())
