from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"AIAS_NEXT158_BUNDLE_RELEASE_AUTHORIZATION_GATE_INSTALLER"
FILES=[ROOT/"src/aias_next158_bundle_release_authorization_gate/__init__.py",ROOT/"src/aias_next158_bundle_release_authorization_gate/gate.py",ROOT/"tests/test_aias_next158_bundle_release_authorization_gate.py",ROOT/"engineering/aias/next158_bundle_release_authorization_gate/AIAS_NEXT_158_SPEC.json",ROOT/"docs/AIAS_NEXT_158_BUNDLE_RELEASE_AUTHORIZATION_GATE.md"]
def main():
 OUT.mkdir(exist_ok=True); m={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}; (OUT/"manifest.json").write_text(json.dumps(m,indent=2)+"\n"); (OUT/"installer.txt").write_text("AIAS_NEXT158_BUNDLE_RELEASE_AUTHORIZATION_GATE_INSTALLER\n"); (OUT/"checksums.sha256").write_text("\n".join(f"{d}  {n}" for n,d in m.items())+"\n"); print(f"AIAS_NEXT158_BUNDLE_RELEASE_AUTHORIZATION_GATE_INSTALLER: {len(FILES)} files checksummed")
if __name__=="__main__": main()
