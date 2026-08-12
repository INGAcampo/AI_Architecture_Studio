from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"AIAS_NEXT159_BUNDLE_AUTHORIZATION_READINESS_INSTALLER"
FILES=[ROOT/"src/aias_next159_bundle_authorization_readiness/__init__.py",ROOT/"src/aias_next159_bundle_authorization_readiness/readiness.py",ROOT/"tests/test_aias_next159_bundle_authorization_readiness.py",ROOT/"engineering/aias/next159_bundle_authorization_readiness/AIAS_NEXT_159_SPEC.json",ROOT/"docs/AIAS_NEXT_159_BUNDLE_AUTHORIZATION_READINESS.md"]
def main():
 OUT.mkdir(exist_ok=True); m={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}; (OUT/"manifest.json").write_text(json.dumps(m,indent=2)+"\n"); (OUT/"installer.txt").write_text("AIAS_NEXT159_BUNDLE_AUTHORIZATION_READINESS_INSTALLER\n"); (OUT/"checksums.sha256").write_text("\n".join(f"{d}  {n}" for n,d in m.items())+"\n"); print(f"AIAS_NEXT159_BUNDLE_AUTHORIZATION_READINESS_INSTALLER: {len(FILES)} files checksummed")
if __name__=="__main__": main()
