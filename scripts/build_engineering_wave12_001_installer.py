from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_ENGINEERING_WAVE12001_ASSURANCE_FOUNDATIONS_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/engineering_wave12"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 for package in ("aias_engineering_wave12","aias_foundation_calcs","aias_foundation_code_checks"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_engineering_wave12_001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/ENGINEERING_WAVE12_001.md",PAYLOAD/"docs")
 for file in (ROOT/"engineering/aias/engineering_wave12").glob("*.json"):shutil.copy2(file,PAYLOAD/"engineering/aias/engineering_wave12")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-ENGINEERING-WAVE12-001","version":"1.0.0","operational_capabilities":["ENG-000004","ENG-000007","ENG-000008","ENG-000009","ENG-000010"],"deferred":[{"id":"ENG-000005","dependency":"ENG-000002"}]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# ENGINEERING-WAVE12-001 Installer\n",encoding="utf-8");(TARGET/"install_engineering_wave12_001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload/src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering/aias/engineering_wave12",r/"engineering/aias/engineering_wave12",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_engineering_wave12_001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_engineering_wave12_001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
