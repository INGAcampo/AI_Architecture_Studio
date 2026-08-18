from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_MEGABLOCK_GEOMETRY2_CONTRACT_INSTALLER"
def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload=TARGET/"payload"
    for rel in ("src/aias_geometry2","src/aias_geometry_kernel","engineering/aias/geometry/GEOMETRY_2_CONTRACT.json","docs/GEOMETRY_2.md","tests/test_geometry2_contract.py"):
        s,d=ROOT/rel,payload/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(s,d,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if s.is_dir() else shutil.copy2(s,d)
    (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"MEGABLOCK-GEOMETRY-2","version":"1.0.0","status":"CONTRACT_IMPLEMENTED_EXTERNAL_KERNEL_PENDING","production_ready":False},indent=2)+"\n",encoding="utf-8")
    files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8"); print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__": main()
