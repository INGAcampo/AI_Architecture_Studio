from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_TECHNICAL_FILE001_ENTERPRISE_DOSSIER_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/technical_file","reference"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 for package in ("aias_technical_file","aias_drawing_framework","aias_engineering_wave12","aias_foundation_calcs","aias_foundation_code_checks","aias_foundation_documentation","aias_foundation_delivery","aias_foundation_handover"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_technical_file001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/TECHNICAL_FILE001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/technical_file/TECHNICAL_FILE_SCHEMA.json",PAYLOAD/"engineering/aias/technical_file");shutil.copy2(ROOT/"technical_file001_reference/release/LIGHTHOUSE-001_TECHNICAL_FILE_R00.zip",PAYLOAD/"reference")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-TECHNICAL-FILE-001","version":"1.0.0","reference":"LIGHTHOUSE-001","status":"FOR_REVIEW","sections":["descriptive_memory","engineering","drawings","documentation","coordination","handover","integrity_manifest"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# TECHNICAL-FILE-001 Installer\n",encoding="utf-8");(TARGET/"install_technical_file001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload/src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering/aias/technical_file",r/"engineering/aias/technical_file",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_technical_file001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_technical_file001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
