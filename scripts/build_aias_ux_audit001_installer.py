from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_UX_AUDIT001_WORKSPACE2_BASELINE_INSTALLER"
PAYLOAD = TARGET / "payload"


def main():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(ROOT / "src/aias_ux_audit", PAYLOAD / "src/aias_ux_audit", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    copies = (
        "engineering/aias/experience/AIAS_UX_AUDIT001_SPEC.json",
        "engineering/aias/experience/AIAS_WORKSPACE2_TARGET_ARCHITECTURE.json",
        "docs/AIAS_UX_AUDIT_001.md",
        "tests/test_aias_ux_audit001.py",
    )
    for relative in copies:
        destination = PAYLOAD / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    from aias_ux_audit import audit_repository
    report = audit_repository(ROOT)
    (TARGET / "audit_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    manifest = {"pack_id": "AIAS-UX-AUDIT-001", "version": "1.0.0", "status": "IMPLEMENTED_EVIDENCE_BASELINE_USABILITY_PENDING", "next": "AIAS-WORKSPACE-2.0-FOUNDATION"}
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files = sorted(path for path in TARGET.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(TARGET).as_posix()}" for path in files) + "\n", encoding="utf-8")
    print(json.dumps({"target": str(TARGET), "files": len(files), "aggregate_evidence_score": report["aggregate_evidence_score"]}))


if __name__ == "__main__":
    main()
