"""Build a checksummed installer payload for AIAS-NEXT-104."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT104_INDEX_REPORT_INSTALLER"
FILES = [ROOT / "src/aias_next104_index_report/__init__.py", ROOT / "src/aias_next104_index_report/report.py", ROOT / "engineering/aias/next104_index_report/AIAS_NEXT_104_SPEC.json", ROOT / "docs/AIAS_NEXT_104_INDEX_INTEGRITY_REPORT.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT104_INDEX_REPORT_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT104_INDEX_REPORT_INSTALLER: {len(FILES)} files checksummed")
