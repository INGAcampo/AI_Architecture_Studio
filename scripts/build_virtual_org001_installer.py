from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_VIRTUAL_ORG001_ENGINEERING_WORKFORCE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/virtual_organization"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_virtual_organization",PAYLOAD/"src/aias_virtual_organization",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_virtual_org001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/VIRTUAL_ORG001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/virtual_organization/VIRTUAL_ENGINEER_ROSTER.json",PAYLOAD/"engineering/aias/virtual_organization")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-VIRTUAL-ORG-001","version":"1.0.0","virtual_engineers":6,"licensed_professionals":0,"outputs":["GOVERNED_ROSTER","COMPETENCY_ROUTING","ACTION_AUTHORIZATION","MAKER_CHECKER","HUMAN_ESCALATION"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# VIRTUAL-ORG-001 Installer\n",encoding="utf-8");(TARGET/"install_virtual_org001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_virtual_organization",r/"src/aias_virtual_organization",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/virtual_organization",r/"engineering/aias/virtual_organization",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_virtual_org001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_virtual_org001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
