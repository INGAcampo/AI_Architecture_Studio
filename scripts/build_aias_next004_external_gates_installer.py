from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_NEXT004_EXTERNAL_GATES_INSTALLER"
def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload=TARGET/"payload"
    for rel in ("engineering/aias/external_gates","docs/AIAS_NEXT_004_EXTERNAL_GATES.md","tests/test_aias_next004_external_gates.py"):
        s,d=ROOT/rel,payload/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(s,d) if s.is_dir() else shutil.copy2(s,d)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-NEXT-004","version":"1.0.0","status":"EVIDENCE_REGISTRY_VALIDATED","external_closure":"PENDING"},indent=2)+"\n",encoding="utf-8")
    fs=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in fs)+"\n",encoding="utf-8"); print(json.dumps({"target":str(TARGET),"files":len(fs)}))
if __name__=="__main__": main()
