from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_EXP_WEB001_OFFICIAL_INFORMATION_ARCHITECTURE_INSTALLER"
PAYLOAD = TARGET / "payload"


def main() -> None:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    entries = (
        "sites/aias-official",
        "engineering/aias/experience/EXP_WEB_001_SPEC.json",
        "docs/EXP_WEB_001.md",
        "tests/test_exp_web001.py",
    )
    for relative in entries:
        source, destination = ROOT / relative, PAYLOAD / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("node_modules", "dist", ".next", ".wrangler", ".dev-*.log"))
        else:
            shutil.copy2(source, destination)
    manifest = {
        "pack_id": "EXP-WEB-001",
        "version": "1.0.0",
        "status": "LOCAL_BUILD_VALIDATED_DEPLOYMENT_APPROVAL_PENDING",
        "external_deployment_performed": False,
        "next": "EXP-APPS-001",
    }
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files = sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name != "checksums.sha256")
    checksums = "\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files) + "\n"
    (TARGET / "checksums.sha256").write_text(checksums, encoding="utf-8")
    print(json.dumps({"target": str(TARGET), "files": len(files)}))


if __name__ == "__main__":
    main()
