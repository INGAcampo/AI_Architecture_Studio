"""Build a checksummed installer payload for AIAS-NEXT-107."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT107_MANIFEST_REPORT_INSTALLER"
FILES = [ROOT / "src/aias_next107_manifest_report/__init__.py", ROOT / "src/aias_next107_manifest_report/report.py", ROOT / "engineering/aias/next107_manifest_report/AIAS_NEXT_107_SPEC.json", ROOT / "docs/AIAS_NEXT_107_MANIFEST_VERIFICATION_REPORT.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT107_MANIFEST_REPORT_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT107_MANIFEST_REPORT_INSTALLER: {len(FILES)} files checksummed")
