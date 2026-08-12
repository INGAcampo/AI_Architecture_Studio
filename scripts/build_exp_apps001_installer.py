from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_EXP_APPS001_SHARED_PLATFORM_CONTRACTS_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/aias_application_platform","engineering/aias/experience/AIAS_APPLICATION_PORTFOLIO.json","engineering/aias/experience/EXP_APPS_001_SPEC.json","engineering/exp_apps001/compliance","docs/EXP_APPS_001.md","tests/test_exp_apps001.py"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"EXP-APPS-001","version":"1.0.0","status":"SHARED_CONTRACT_FOUNDATION_VALIDATED","public_apps_deployed":False,"next":"EXP-PLATFORM-GUI-001","deferred":["EXP-COMMS-001"]},indent=2)+"\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
