from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_LEVEL5_ASSURANCE001_MATURITY_ASSURANCE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/level5"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_level5_assurance",PAYLOAD/"src/aias_level5_assurance",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_level5_assurance001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/LEVEL5_ASSURANCE001.md",PAYLOAD/"docs")
 for file in (ROOT/"engineering/aias/level5").glob("*.json"):shutil.copy2(file,PAYLOAD/"engineering/aias/level5")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-LEVEL5-ASSURANCE-001","version":"1.0.0","reference_capability_level":5,"audited_organizational_level":None,"outputs":["EVIDENCE_CLASSIFICATION","LONGITUDINAL_POLICY","METRIC_THRESHOLDS","INDEPENDENT_AUDIT_GATE","REFERENCE_ASSESSMENT"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# LEVEL5-ASSURANCE-001 Installer\n",encoding="utf-8");(TARGET/"install_level5_assurance001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_level5_assurance",r/"src/aias_level5_assurance",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/level5",r/"engineering/aias/level5",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_level5_assurance001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_level5_assurance001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
