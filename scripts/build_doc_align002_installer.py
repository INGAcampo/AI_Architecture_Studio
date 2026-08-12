from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_DOC_ALIGN_002_COMPLETE_PUBLIC_API_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","scripts"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 for package in sorted((ROOT/"src").glob("aias_*")):
  if package.is_dir():shutil.copytree(package,PAYLOAD/"src"/package.name,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 for name in ("test_doc_align002.py","test_gov000049_governance_assurance.py"):shutil.copy2(ROOT/"tests"/name,PAYLOAD/"tests")
 shutil.copy2(ROOT/"docs"/"DOC_ALIGN_002_COMPLETE_PUBLIC_API.md",PAYLOAD/"docs");shutil.copy2(ROOT/"scripts"/"align_public_api_documentation.py",PAYLOAD/"scripts")
 manifest={"pack_id":"AIAS-DOC-ALIGN-002","version":"1.0.0","outputs":["COMPLETE_PUBLIC_API_DOCUMENTATION","METHOD_LEVEL_AUDIT","RISK_PRIORITY_PLAN","DRIFT_GATE"],"measured_baseline":{"modules":327,"public_symbols_including_methods":934,"documentation_debt":0}}
 (TARGET/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# DOC-ALIGN-002 Installer\n\nInstala la línea base documental completa y ejecuta la puerta anti-deriva.\n",encoding="utf-8");(TARGET/"install_doc_align002.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload"/"src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
for test in (h/"payload"/"tests").glob("*.py"):shutil.copy2(test,r/"tests")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_doc_align002.py"),str(r/"tests"/"test_gov000049_governance_assurance.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
