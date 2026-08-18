from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_DOC_ALIGN_001_ACTIVE_PACKAGES_INSTALLER";PAYLOAD=TARGET/"payload";PACKAGES=("aias_foundation_handover","aias_technology_observatory","aias_governance_assurance")
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 (PAYLOAD/"src").mkdir(parents=True);(PAYLOAD/"tests").mkdir();(PAYLOAD/"docs").mkdir()
 for package in PACKAGES:shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 for test in ("test_ecp000001f_foundation_handover.py","test_ecp000001g_technology_observatory.py","test_gov000049_governance_assurance.py"):shutil.copy2(ROOT/"tests"/test,PAYLOAD/"tests")
 shutil.copy2(ROOT/"docs"/"DOC_ALIGN_001_ACTIVE_PACKAGES.md",PAYLOAD/"docs")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-DOC-ALIGN-001","version":"1.0.0","packages":PACKAGES,"documented_modules":26,"documented_public_symbols":29,"quality_gate":"NO_DOCUMENTATION_REGRESSION"},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# DOC-ALIGN-001 Installer\n\nInstala la documentación de tres paquetes activos y ejecuta sus regresiones.\n",encoding="utf-8");(TARGET/"install_doc_align_001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in ("aias_foundation_handover","aias_technology_observatory","aias_governance_assurance"):shutil.copytree(h/"payload"/"src"/package,r/"src"/package,dirs_exist_ok=True)
tests=[str(r/"tests"/x) for x in ("test_ecp000001f_foundation_handover.py","test_ecp000001g_technology_observatory.py","test_gov000049_governance_assurance.py")];raise SystemExit(subprocess.run([sys.executable,"-m","pytest",*tests,"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
