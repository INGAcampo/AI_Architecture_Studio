"""Build a checksummed installer payload for AIAS-NEXT-101."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT101_INDEX_INSTALLER"
FILES = [ROOT / "src/aias_next101_index/__init__.py", ROOT / "src/aias_next101_index/index.py", ROOT / "engineering/aias/next101_index/AIAS_NEXT_101_SPEC.json", ROOT / "docs/AIAS_NEXT_101_RELEASE_ARTIFACT_INDEX.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT101_INDEX_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT101_INDEX_INSTALLER: {len(FILES)} files checksummed")
