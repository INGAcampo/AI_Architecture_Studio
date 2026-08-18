from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_GEOMETRY_2_0_A_002_POC_INSTALLER"
def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload=TARGET/"payload"
    for rel in ("engineering/aias/geometry/GEOMETRY_2_0_A_002_POC.json","docs/GEOMETRY_2_0_A_002.md","tests/test_geometry_2_0_a_002.py"):
        s,d=ROOT/rel,payload/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(s,d)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"GEOMETRY-2.0-A-002","version":"1.0.0","status":"POC_EXECUTED_RUNTIME_UNAVAILABLE","production_ready":False},indent=2)+"\n",encoding="utf-8")
    fs=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in fs)+"\n",encoding="utf-8"); print(json.dumps({"target":str(TARGET),"files":len(fs)}))
if __name__=="__main__": main()
