from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_END_TO_END001_PROJECT_PRODUCTION_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/end_to_end"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 packages=("aias_end_to_end","aias_autonomous_cloud","aias_central_nervous_system","aias_engineering_os","aias_security_recovery","aias_technical_file","aias_virtual_organization")
 for package in packages:shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_end_to_end001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/END_TO_END001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/end_to_end/END_TO_END_CONTRACT.json",PAYLOAD/"engineering/aias/end_to_end")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-END-TO-END-001","version":"1.0.0","reference_project":"LIGHTHOUSE-001","status":"OPERATING_REFERENCE_FOR_REVIEW","outputs":["TECHNICAL_FILE","INDEPENDENT_REVIEW","AEOS_OPERATING","CNS_EVENTS","RECOVERY_DRILL","CLOUD_CUSTODY"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# END-TO-END-001 Installer\n",encoding="utf-8");(TARGET/"install_end_to_end001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload/src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering/aias/end_to_end",r/"engineering/aias/end_to_end",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_end_to_end001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_end_to_end001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
