"""Build a checksummed installer payload for AIAS-NEXT-123."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT123_FEED_INDEX_INTEGRITY_INSTALLER"
FILES = [ROOT / "src/aias_next123_feed_index_integrity/__init__.py", ROOT / "src/aias_next123_feed_index_integrity/integrity.py", ROOT / "engineering/aias/next123_feed_index_integrity/AIAS_NEXT_123_SPEC.json", ROOT / "docs/AIAS_NEXT_123_FEED_INDEX_INTEGRITY.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT123_FEED_INDEX_INTEGRITY_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT123_FEED_INDEX_INTEGRITY_INSTALLER: {len(FILES)} files checksummed")
