from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_AIPD000001_PRODUCTIVITY_DASHBOARD_INSTALLER";PAYLOAD=TARGET/"payload"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_productivity_dashboard",PAYLOAD/"src"/"aias_productivity_dashboard",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_aipd000001_productivity_dashboard.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"AIPD000001_PRODUCTIVITY_DASHBOARD.md",PAYLOAD/"docs")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-AIPD-000001","version":"1.1.0","outputs":["HTML_DASHBOARD","JSON_SNAPSHOT","RELEASE_ZIP","EXTERNAL_GATE_PANEL"],"permanent_panel":True,"evidence_derived":True,"level_5_claim_controlled":True},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# AIAS Productivity Dashboard Installer v1.1.0\n\nInstala el panel permanente, incluidas las compuertas externas verificables.\n",encoding="utf-8");(TARGET/"install_aipd000001.py").write_text(INSTALLER,encoding="utf-8");(TARGET/"run_dashboard.py").write_text(RUNNER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_productivity_dashboard",r/"src"/"aias_productivity_dashboard",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_aipd000001_productivity_dashboard.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_aipd000001_productivity_dashboard.py"),"-q"],cwd=r).returncode)
'''
RUNNER='''from pathlib import Path
from aias_productivity_dashboard.orchestrator import ProductivityDashboardOrchestrator
print(ProductivityDashboardOrchestrator().execute(Path(".").resolve(),Path("aias_productivity_dashboard_outputs").resolve()))
'''
if __name__=="__main__":main()
