from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_GOV000049_HISTORICAL_DECISION_SDD_ASSURANCE_INSTALLER";PAYLOAD=TARGET/"payload"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs","engineering"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_governance_assurance",PAYLOAD/"src"/"aias_governance_assurance",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_gov000049_governance_assurance.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"GOV000049_HISTORICAL_DECISION_MATERIALIZATION.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering"/"aeps"/"05_SDD"/"ASDD-000003-code-documentation-standard.yaml",PAYLOAD/"engineering")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-GOV-000049","version":"1.0.0","outputs":["DECISION_MATRIX","DOCUMENTATION_COVERAGE","SDD_ASSURANCE","AMDP","ALIGNMENT_BACKLOG"],"honest_legacy_baseline":True},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# GOV-000049 Installer\n\nInstala la auditoría de decisiones, documentación y SDD sin modificar código legado.\n",encoding="utf-8");(TARGET/"install_gov000049.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_governance_assurance",r/"src"/"aias_governance_assurance",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_gov000049_governance_assurance.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_gov000049_governance_assurance.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
