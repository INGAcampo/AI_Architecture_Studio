"""Build a checksummed installer payload for AIAS-NEXT-090."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT090_DASHBOARD_INTEGRATION_INSTALLER"
FILES = [ROOT / "src/aias_next090_dashboard_integration/__init__.py", ROOT / "src/aias_next090_dashboard_integration/integration.py", ROOT / "engineering/aias/next090_dashboard_integration/AIAS_NEXT_090_SPEC.json", ROOT / "docs/AIAS_NEXT_090_EVIDENCE_REVIEW_DASHBOARD_INTEGRATION.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT090_DASHBOARD_INTEGRATION_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT090_DASHBOARD_INTEGRATION_INSTALLER: {len(FILES)} files checksummed")
