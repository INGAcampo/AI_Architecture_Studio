"""Build a checksummed installer payload for AIAS-NEXT-085."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT085_DECISION_AUDIT_INSTALLER"
FILES = [ROOT / "src/aias_next085_decision_audit/__init__.py", ROOT / "src/aias_next085_decision_audit/audit.py", ROOT / "engineering/aias/next085_decision_audit/AIAS_NEXT_085_SPEC.json", ROOT / "docs/AIAS_NEXT_085_DECISION_AUDIT.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT085_DECISION_AUDIT_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT085_DECISION_AUDIT_INSTALLER: {len(FILES)} files checksummed")
