"""Build the checksummed AIAS-NEXT-133 installer manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT133_BUNDLE_INSTALLER"
FILES = [
    ROOT / "src/aias_next133_bundle/__init__.py",
    ROOT / "src/aias_next133_bundle/bundle.py",
    ROOT / "tests/test_aias_next133_bundle.py",
    ROOT / "engineering/aias/next133_bundle/AIAS_NEXT_133_SPEC.json",
    ROOT / "docs/AIAS_NEXT_133_BUNDLE_RELEASE_EVIDENCE.md",
]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    manifest = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in FILES
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "installer.txt").write_text("AIAS_NEXT133_BUNDLE_INSTALLER\n", encoding="utf-8")
    checksums = "\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n"
    (OUT / "checksums.sha256").write_text(checksums, encoding="utf-8")
    print(f"AIAS_NEXT133_BUNDLE_INSTALLER: {len(FILES)} files checksummed")


if __name__ == "__main__":
    main()
