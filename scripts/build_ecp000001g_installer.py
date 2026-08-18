from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_ECP000001G_TECHNOLOGY_OBSERVATORY_INSTALLER";PAYLOAD=TARGET/"payload"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_technology_observatory",PAYLOAD/"src"/"aias_technology_observatory",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_ecp000001g_technology_observatory.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"ECP000001G_AIAS_TECHNOLOGY_OBSERVATORY.md",PAYLOAD/"docs")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-ECP-000001G-ATO","version":"1.0.0","article":"AEC-000049","consumes":["ECP-000001F"],"outputs":["SOURCE_LEDGER","OPPORTUNITY_PORTFOLIO","NIST_AIRMF_ADAPTER","RELEASE_ZIP"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# ATO Installer\n\nInstala el observatorio y ejecuta su validación enfocada.\n",encoding="utf-8");(TARGET/"install_ecp000001g.py").write_text(INSTALLER,encoding="utf-8");(TARGET/"run_ecp000001g.py").write_text(RUNNER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_technology_observatory",r/"src"/"aias_technology_observatory",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_ecp000001g_technology_observatory.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_ecp000001g_technology_observatory.py"),"-q"],cwd=r).returncode)
'''
RUNNER='''from pathlib import Path
from aias_technology_observatory.orchestrator import TechnologyObservatoryOrchestrator
print(TechnologyObservatoryOrchestrator().execute(Path("ecp000001g_outputs").resolve()))
'''
if __name__=="__main__":main()
