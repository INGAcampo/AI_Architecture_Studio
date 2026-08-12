from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_FOUNDATION_ALIGN002_ENGINEERING_SYSTEM_AES_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/foundation"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_engineering_system",PAYLOAD/"src"/"aias_engineering_system",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_foundation_align002.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"FOUNDATION_ALIGN002_ENGINEERING_SYSTEM_AES.md",PAYLOAD/"docs")
 for name in ("AIAS_ENGINEERING_SYSTEM.json","AIAS_AES_STANDARDS_REGISTRY.json"):shutil.copy2(ROOT/"engineering"/"aias"/"foundation"/name,PAYLOAD/"engineering"/"aias"/"foundation")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-FOUNDATION-ALIGN-002","version":"1.0.0","outputs":["ENGINEERING_SYSTEM","AES_STANDARDS_REGISTRY","EXECUTABLE_VALIDATOR"]},indent=2)+"\n",encoding="utf-8")
 (TARGET/"README_INSTALACION.md").write_text("# FOUNDATION-ALIGN-002 Installer\n\nEngineering System y AES ejecutables.\n",encoding="utf-8")
 (TARGET/"install_foundation_align002.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload"/"src"/"aias_engineering_system",r/"src"/"aias_engineering_system",dirs_exist_ok=True)
shutil.copytree(h/"payload"/"engineering"/"aias"/"foundation",r/"engineering"/"aias"/"foundation",dirs_exist_ok=True)
shutil.copy2(h/"payload"/"tests"/"test_foundation_align002.py",r/"tests")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_foundation_align002.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
