from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_WORKSPACE2_W2_06_COORDINATION_LEARNING_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/gui/workspace2","engineering/aias/experience/AIAS_WORKSPACE2_W2_06_SPEC.json","engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json","docs/AIAS_WORKSPACE2_W2_06.md","tests/test_aias_workspace2_w2_06.py","workspace2_w2_06_outputs/COORDINATION_LEARNING.html","workspace2_w2_06_outputs/COORDINATION_LEARNING.json"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-WORKSPACE-2.0-W2-06","version":"0.6.0","status":"IMPLEMENTED_VALIDATED","next":"W2-07"},indent=2)+"\n",encoding="utf-8");files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
