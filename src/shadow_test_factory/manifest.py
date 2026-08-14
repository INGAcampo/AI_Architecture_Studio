from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    file_path = Path(path)
    digest = hashlib.sha256()

    with file_path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def build_manifest(root: str | Path) -> list[dict]:
    base = Path(root)
    entries = []

    for file_path in sorted(item for item in base.rglob("*") if item.is_file()):
        entries.append(
            {
                "path": file_path.relative_to(base).as_posix(),
                "bytes": file_path.stat().st_size,
                "sha256": sha256_file(file_path),
            }
        )

    return entries
