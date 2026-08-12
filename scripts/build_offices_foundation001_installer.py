from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_OFFICES_FOUNDATION001_ENTERPRISE_OFFICES_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/offices"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_enterprise_offices",PAYLOAD/"src/aias_enterprise_offices",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_offices_foundation001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/OFFICES_FOUNDATION001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/offices/ENTERPRISE_OFFICE_CHARTERS.json",PAYLOAD/"engineering/aias/offices")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-OFFICES-FOUNDATION-001","version":"1.0.0","operational_offices":10,"deferred_offices":["OFFICE-000005"],"outputs":["OFFICE_CHARTERS","ACCOUNTABILITY_ROUTING","DECISION_RIGHTS","EVIDENCE_GATES","KPI_MANDATES"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# OFFICES-FOUNDATION-001 Installer\n",encoding="utf-8");(TARGET/"install_offices_foundation001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_enterprise_offices",r/"src/aias_enterprise_offices",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/offices",r/"engineering/aias/offices",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_offices_foundation001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_offices_foundation001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
