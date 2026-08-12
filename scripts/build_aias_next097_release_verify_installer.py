"""Build a checksummed installer payload for AIAS-NEXT-097."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AIAS_NEXT097_RELEASE_VERIFY_INSTALLER"
FILES = [ROOT / "src/aias_next097_release_verify/__init__.py", ROOT / "src/aias_next097_release_verify/verify.py", ROOT / "engineering/aias/next097_release_verify/AIAS_NEXT_097_SPEC.json", ROOT / "docs/AIAS_NEXT_097_RELEASE_PACKAGE_VERIFICATION.md"]
OUT.mkdir(exist_ok=True)
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(OUT / "manifest.json").write_text(json.dumps({"installer": "AIAS_NEXT097_RELEASE_VERIFY_INSTALLER", "files": manifest}, indent=2), encoding="utf-8")
(OUT / "checksums.sha256").write_text("\n".join(f"{digest}  {name}" for name, digest in manifest.items()) + "\n", encoding="utf-8")
print(f"AIAS_NEXT097_RELEASE_VERIFY_INSTALLER: {len(FILES)} files checksummed")
