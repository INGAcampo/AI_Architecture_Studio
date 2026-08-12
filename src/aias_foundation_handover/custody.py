"""Checksum verification and append-only custody-event construction."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from .models import CustodyEvent

def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_transmittal(transmittal: Path) -> dict:
    """Verify every file declared by an ECP-000001E transmittal manifest."""
    manifest_path = transmittal / "TRANSMITTAL_MANIFEST.json"
    if not manifest_path.is_file(): raise FileNotFoundError("missing_transmittal_manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {row["path"]: row["sha256"] for row in manifest["revision_manifest"]["files"]}
    checked, missing, mismatched = [], [], []
    for relative, digest in expected.items():
        path = transmittal / relative
        if not path.is_file(): missing.append(relative)
        elif sha256(path) != digest: mismatched.append(relative)
        else: checked.append(relative)
    return {"valid": not missing and not mismatched, "package_id": manifest["package_id"], "checked_count": len(checked), "missing": missing, "mismatched": mismatched, "manifest": manifest}

def custody_event(package_id: str, actor: str, previous_hash: str = "GENESIS") -> CustodyEvent:
    """Create a hash-linked custody acceptance event for ``package_id``."""
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = json.dumps({"action":"HANDOVER_ACCEPTED","actor":actor,"package_id":package_id,"previous_hash":previous_hash,"timestamp_utc":timestamp}, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return CustodyEvent(f"CUST-{digest[:12].upper()}", timestamp, "HANDOVER_ACCEPTED", package_id, actor, previous_hash, digest)
