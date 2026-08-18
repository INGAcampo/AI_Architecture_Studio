"""Build the checksummed AIAS-NEXT-156 installer manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT156_BUNDLE_RELEASE_AUTHORIZATION_INSTALLER"
FILES = [
    ROOT / "src/aias_next156_bundle_release_authorization/__init__.py",
    ROOT / "src/aias_next156_bundle_release_authorization/authorization.py",
    ROOT / "tests/test_aias_next156_bundle_release_authorization.py",
    ROOT / "engineering/aias/next156_bundle_release_authorization/AIAS_NEXT_156_SPEC.json",
    ROOT / "docs/AIAS_NEXT_156_BUNDLE_RELEASE_AUTHORIZATION.md",
]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    manifest = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in FILES}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "installer.txt").write_text("AIAS_NEXT156_BUNDLE_RELEASE_AUTHORIZATION_INSTALLER\n", encoding="utf-8")
    (OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
    print(f"AIAS_NEXT156_BUNDLE_RELEASE_AUTHORIZATION_INSTALLER: {len(FILES)} files checksummed")


if __name__ == "__main__":
    main()
