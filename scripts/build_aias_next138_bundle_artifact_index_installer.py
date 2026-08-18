"""Build the checksummed AIAS-NEXT-138 installer manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT138_BUNDLE_ARTIFACT_INDEX_INSTALLER"
FILES = [
    ROOT / "src/aias_next138_bundle_artifact_index/__init__.py",
    ROOT / "src/aias_next138_bundle_artifact_index/index.py",
    ROOT / "tests/test_aias_next138_bundle_artifact_index.py",
    ROOT / "engineering/aias/next138_bundle_artifact_index/AIAS_NEXT_138_SPEC.json",
    ROOT / "docs/AIAS_NEXT_138_BUNDLE_ARTIFACT_INDEX.md",
]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    manifest = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in FILES}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "installer.txt").write_text("AIAS_NEXT138_BUNDLE_ARTIFACT_INDEX_INSTALLER\n", encoding="utf-8")
    (OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
    print(f"AIAS_NEXT138_BUNDLE_ARTIFACT_INDEX_INSTALLER: {len(FILES)} files checksummed")


if __name__ == "__main__":
    main()
