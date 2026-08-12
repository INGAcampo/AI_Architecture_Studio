"""Build a checksummed installer payload for AIAS-NEXT-128."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT128_FEED_GATE_INSTALLER"
FILES = [ROOT / "src/aias_next128_feed_gate/__init__.py", ROOT / "src/aias_next128_feed_gate/gate.py", ROOT / "engineering/aias/next128_feed_gate/AIAS_NEXT_128_SPEC.json", ROOT / "docs/AIAS_NEXT_128_FEED_BUNDLE_RELEASE_GATE.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT128_FEED_GATE_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT128_FEED_GATE_INSTALLER: {len(FILES)} files checksummed")
