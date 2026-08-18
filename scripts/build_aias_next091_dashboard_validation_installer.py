"""Build a checksummed installer payload for AIAS-NEXT-091."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT091_DASHBOARD_VALIDATION_INSTALLER"
FILES = [ROOT / "src/aias_next091_dashboard_validation/__init__.py", ROOT / "src/aias_next091_dashboard_validation/validation.py", ROOT / "engineering/aias/next091_dashboard_validation/AIAS_NEXT_091_SPEC.json", ROOT / "docs/AIAS_NEXT_091_DASHBOARD_INTEGRATION_VALIDATION.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT091_DASHBOARD_VALIDATION_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT091_DASHBOARD_VALIDATION_INSTALLER: {len(FILES)} files checksummed")
