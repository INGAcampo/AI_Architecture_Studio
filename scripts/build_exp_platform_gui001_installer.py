from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_EXP_PLATFORM_GUI001_CAPABILITY_CENTER_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/gui/workspace2/capability_center.py","src/gui/workspace2/commanding.py","src/gui/workspace2/__init__.py","engineering/aias/experience/EXP_PLATFORM_GUI_001_SPEC.json","engineering/exp_platform_gui001/compliance","docs/EXP_PLATFORM_GUI_001.md","tests/test_exp_platform_gui001.py","scripts/render_exp_platform_gui001.py","exp_platform_gui001_outputs"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"EXP-PLATFORM-GUI-001","version":"1.0.0","status":"VALIDATED_APPLICATION_VISIBLE_FOUNDATION","mutating_actions_enabled":False,"publisher_signed":False,"next":"GOV-VERTICAL-ENFORCEMENT-001"},indent=2)+"\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
