"""Build a checksummed installer payload for AIAS-NEXT-080."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT080_INTAKE_INSTALLER"
FILES = [ROOT / "src/aias_next080_intake/__init__.py", ROOT / "src/aias_next080_intake/intake.py", ROOT / "engineering/aias/next080_intake/AIAS_NEXT_080_SPEC.json", ROOT / "docs/AIAS_NEXT_080_EXTERNAL_EVIDENCE_INTAKE.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT080_INTAKE_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT080_INTAKE_INSTALLER: {len(FILES)} files checksummed")
