"""Normalize checksum manifests for every materialized AIAS installer."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize(installer: Path) -> int:
    """Write a deterministic manifest covering every current non-cache installer file."""
    files = sorted(
        path
        for path in installer.rglob("*")
        if path.is_file()
        and path.name != "checksums.sha256"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(installer).as_posix()}"
        for path in files
    ]
    (installer / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(files)


def main() -> None:
    """Normalize every installer and print an auditable aggregate result."""
    installers = sorted(path for path in ROOT.glob("AIAS_*_INSTALLER") if path.is_dir())
    rows = [{"installer": path.name, "files": normalize(path)} for path in installers]
    print({"installers": len(rows), "files": sum(row["files"] for row in rows)})


if __name__ == "__main__":
    main()
