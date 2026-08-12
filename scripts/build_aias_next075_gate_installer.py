"""Build a checksummed installer payload for AIAS-NEXT-075."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT075_GATE_INSTALLER"
FILES = [ROOT / "src/aias_next075_gate/__init__.py", ROOT / "src/aias_next075_gate/gate.py", ROOT / "engineering/aias/next075_gate/AIAS_NEXT_075_SPEC.json", ROOT / "docs/AIAS_NEXT_075_PUBLICATION_EVIDENCE_GATE.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT075_GATE_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT075_GATE_INSTALLER: {len(FILES)} files checksummed")
