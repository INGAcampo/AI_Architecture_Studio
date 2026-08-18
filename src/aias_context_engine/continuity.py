"""Checksum-protected conversation continuity package generation and validation."""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = ("MASTER_CONTEXT.json", "PROJECT_STATE.json", "NEXT_TASK.yaml", "CONTINUE_PROMPT.md", "EXECUTIVE_ORDERS.md")


def create_continuity_package(ackc: Path, output: Path) -> dict:
    """Package the validated minimum ACE handoff evidence for a new primary conversation."""
    ackc = Path(ackc)
    missing = [name for name in REQUIRED if not (ackc / name).is_file()]
    if missing:
        raise ValueError(f"missing_continuity_evidence:{','.join(missing)}")
    context = json.loads((ackc / "MASTER_CONTEXT.json").read_text(encoding="utf-8"))
    if not context.get("integrity", {}).get("canonical_payload_sha256"):
        raise ValueError("unvalidated_master_context")
    checksums = {name: hashlib.sha256((ackc / name).read_bytes()).hexdigest() for name in REQUIRED}
    manifest = {
        "package_id": "AIAS-CONTINUITY-HANDOFF",
        "article": "AEC-000051",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "current": context["roadmap"]["current"],
        "next": context["roadmap"]["next"],
        "source_context_integrity": context["integrity"]["canonical_payload_sha256"],
        "files": checksums,
        "status": "READY_FOR_VERIFIED_RESUME",
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in REQUIRED:
            bundle.write(ackc / name, name)
        bundle.writestr("MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        bundle.writestr("checksums.sha256", "\n".join(f"{digest}  {name}" for name, digest in checksums.items()) + "\n")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    Path(str(output) + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return {"package": str(output), "sha256": digest, "files": len(REQUIRED), "status": manifest["status"]}


def validate_continuity_package(package: Path) -> dict:
    """Verify package structure, individual file hashes and the external archive checksum when present."""
    package = Path(package)
    errors: list[str] = []
    with zipfile.ZipFile(package) as bundle:
        names = set(bundle.namelist())
        for required in (*REQUIRED, "MANIFEST.json", "checksums.sha256"):
            if required not in names:
                errors.append(f"missing:{required}")
        if not errors:
            manifest = json.loads(bundle.read("MANIFEST.json"))
            if manifest.get("article") != "AEC-000051" or manifest.get("status") != "READY_FOR_VERIFIED_RESUME":
                errors.append("invalid_manifest")
            for name, expected in manifest.get("files", {}).items():
                if hashlib.sha256(bundle.read(name)).hexdigest() != expected:
                    errors.append(f"checksum:{name}")
    sidecar = Path(str(package) + ".sha256")
    if sidecar.is_file() and hashlib.sha256(package.read_bytes()).hexdigest() != sidecar.read_text(encoding="utf-8-sig").split()[0]:
        errors.append("archive_checksum")
    return {"valid": not errors, "errors": errors}
