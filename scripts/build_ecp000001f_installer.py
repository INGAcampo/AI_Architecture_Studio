from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TARGET=ROOT/"AIAS_ECP000001F_FOUNDATION_DIGITAL_HANDOVER_INSTALLER"; PAYLOAD=TARGET/"payload"
def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def main()->None:
    if TARGET.exists():shutil.rmtree(TARGET)
    for folder in ("src","tests","docs"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/"src"/"aias_foundation_handover",PAYLOAD/"src"/"aias_foundation_handover",ignore=shutil.ignore_patterns("__pycache__","*.pyc","*.pyo"))
    shutil.copy2(ROOT/"tests"/"test_ecp000001f_foundation_handover.py",PAYLOAD/"tests"); shutil.copy2(ROOT/"docs"/"ECP000001F_FOUNDATION_DIGITAL_HANDOVER.md",PAYLOAD/"docs")
    manifest={"pack_id":"AIAS-ECP-000001F-FOUNDATION-DIGITAL-HANDOVER","version":"1.0.0","expected_focused_tests":10,"consumes":["ECP-000001E"],"outputs":["LIFECYCLE_DOSSIER","CUSTODY_LEDGER","ACCEPTANCE_GATES","MATURITY_EVIDENCE","KPI_EVIDENCE","RELEASE_ZIP"],"level_5_claim":"REFERENCE_CASE_CAPABILITY","construction_approval_inherited_only":True}
    (TARGET/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8"); (TARGET/"README_INSTALACION.md").write_text("# ECP-000001F Installer\n\nInstala el paquete, ejecuta sus pruebas y conserva los controles de aprobación profesional.\n",encoding="utf-8"); (TARGET/"install_ecp000001f.py").write_text(INSTALLER,encoding="utf-8"); (TARGET/"run_ecp000001f.py").write_text(RUNNER,encoding="utf-8")
    files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256"); (TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8"); print(TARGET)
INSTALLER=r'''from __future__ import annotations
import argparse,shutil,subprocess,sys
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();here=Path(__file__).resolve().parent;root=Path(a.project_root).resolve();payload=here/"payload";shutil.copytree(payload/"src"/"aias_foundation_handover",root/"src"/"aias_foundation_handover",dirs_exist_ok=True);shutil.copy2(payload/"tests"/"test_ecp000001f_foundation_handover.py",root/"tests");shutil.copy2(payload/"docs"/"ECP000001F_FOUNDATION_DIGITAL_HANDOVER.md",root/"docs");return subprocess.run([sys.executable,"-m","pytest",str(root/"tests"/"test_ecp000001f_foundation_handover.py"),"-q"],cwd=root).returncode
if __name__=="__main__":raise SystemExit(main())
'''
RUNNER=r'''from pathlib import Path
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator
if __name__=="__main__":print(FoundationHandoverOrchestrator().execute(Path("ecp000001f_outputs").resolve()))
'''
if __name__=="__main__":main()
