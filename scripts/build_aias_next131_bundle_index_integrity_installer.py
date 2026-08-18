"""Build a checksummed installer payload for AIAS-NEXT-131."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT131_BUNDLE_INDEX_INTEGRITY_INSTALLER"
FILES = [ROOT / "src/aias_next131_bundle_index_integrity/__init__.py", ROOT / "src/aias_next131_bundle_index_integrity/integrity.py", ROOT / "engineering/aias/next131_bundle_index_integrity/AIAS_NEXT_131_SPEC.json", ROOT / "docs/AIAS_NEXT_131_BUNDLE_INDEX_INTEGRITY.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT131_BUNDLE_INDEX_INTEGRITY_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT131_BUNDLE_INDEX_INTEGRITY_INSTALLER: {len(FILES)} files checksummed")
