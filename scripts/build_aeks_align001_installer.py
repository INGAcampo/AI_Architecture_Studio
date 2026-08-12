from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_AEKS_ALIGN001_EXECUTABLE_KNOWLEDGE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs","engineering/aias/aeks"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 for package in ("aias_aeks","aias_executable_knowledge"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests"/"test_aeks_align001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"AEKS_ALIGN001_EXECUTABLE_KNOWLEDGE.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering"/"aias"/"aeks"/"EKU-000002-bearing-pressure.json",PAYLOAD/"engineering"/"aias"/"aeks")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-AEKS-ALIGN-001","version":"1.0.0","outputs":["KNOWLEDGE_ADMISSION","SAFE_DECLARATIVE_EXECUTOR","EXECUTION_EVIDENCE","REFERENCE_EKU"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# AEKS-ALIGN-001 Installer\n",encoding="utf-8");(TARGET/"install_aeks_align001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload"/"src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload"/"engineering"/"aias"/"aeks",r/"engineering"/"aias"/"aeks",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_aeks_align001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_aeks_align001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
