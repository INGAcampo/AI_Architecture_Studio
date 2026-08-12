from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_GEOMETRY_BIM_BRIDGE002_TESSELLATION_INSTALLER"
def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload=TARGET/"payload"
    for rel in ("src/aias_geometry_bim_bridge","engineering/aias/bridge/GEOMETRY_BIM_BRIDGE_002_EVIDENCE.json","docs/GEOMETRY_BIM_BRIDGE_002.md","tests/test_geometry_bim_bridge_002.py"):
        s,d=ROOT/rel,payload/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(s,d) if s.is_dir() else shutil.copy2(s,d)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"GEOMETRY-BIM-BRIDGE-002","version":"1.0.0","status":"DETERMINISTIC_PREVIEW_TESSELLATION_VALIDATED","production_brep":False},indent=2)+"\n",encoding="utf-8")
    fs=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in fs)+"\n",encoding="utf-8"); print(json.dumps({"target":str(TARGET),"files":len(fs)}))
if __name__=="__main__": main()
