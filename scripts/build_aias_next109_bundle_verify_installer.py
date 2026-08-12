"""Build a checksummed installer payload for AIAS-NEXT-109."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT109_BUNDLE_VERIFY_INSTALLER"
FILES = [ROOT / "src/aias_next109_bundle_verify/__init__.py", ROOT / "src/aias_next109_bundle_verify/verify.py", ROOT / "engineering/aias/next109_bundle_verify/AIAS_NEXT_109_SPEC.json", ROOT / "docs/AIAS_NEXT_109_BUNDLE_VERIFICATION.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT109_BUNDLE_VERIFY_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT109_BUNDLE_VERIFY_INSTALLER: {len(FILES)} files checksummed")
