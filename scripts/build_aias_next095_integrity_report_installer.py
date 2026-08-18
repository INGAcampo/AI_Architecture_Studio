"""Build a checksummed installer payload for AIAS-NEXT-095."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT095_INTEGRITY_REPORT_INSTALLER"
FILES = [ROOT / "src/aias_next095_integrity_report/__init__.py", ROOT / "src/aias_next095_integrity_report/report.py", ROOT / "engineering/aias/next095_integrity_report/AIAS_NEXT_095_SPEC.json", ROOT / "docs/AIAS_NEXT_095_INTEGRITY_VERIFICATION_REPORT.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT095_INTEGRITY_REPORT_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT095_INTEGRITY_REPORT_INSTALLER: {len(FILES)} files checksummed")
