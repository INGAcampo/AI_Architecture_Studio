"""Build a checksummed installer payload for AIAS-NEXT-120."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT120_FEED_GATE_INSTALLER"
FILES = [ROOT / "src/aias_next120_feed_gate/__init__.py", ROOT / "src/aias_next120_feed_gate/gate.py", ROOT / "engineering/aias/next120_feed_gate/AIAS_NEXT_120_SPEC.json", ROOT / "docs/AIAS_NEXT_120_FEED_RELEASE_READINESS_GATE.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT120_FEED_GATE_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT120_FEED_GATE_INSTALLER: {len(FILES)} files checksummed")
