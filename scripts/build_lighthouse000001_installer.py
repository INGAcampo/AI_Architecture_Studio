from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_LIGHTHOUSE000001_REFERENCE_BUILDING_INSTALLER";PAYLOAD=TARGET/"payload"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_lighthouse_project",PAYLOAD/"src"/"aias_lighthouse_project",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_lighthouse000001_reference_building.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"LIGHTHOUSE000001_REFERENCE_BUILDING.md",PAYLOAD/"docs")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-LIGHTHOUSE-000001","version":"1.4.0","jurisdiction":"Venezuela","jurisdiction_profile_id":"VE-001","consumes":["ECP-000001A","ECP-000001B","ECP-000001C","ECP-000001D","ECP-000001E","ECP-000001F","STRUCTURAL-CODES-PROGRAM-001","CAD-BIM-INTEGRATION-001"],"outputs":["PROJECT_BRIEF","WHOLE_BUILDING_STRUCTURAL_REPORT","REFERENCE_LOAD_COMBINATIONS","WHOLE_BUILDING_BIM_IFC_NEUTRAL","STRUCTURAL_PLAN","STRUCTURAL_ELEVATION","BEAM_SCHEDULE","COLUMN_SCHEDULE","FOUNDATION_SCHEDULE","STRUCTURAL_QUANTITIES","MEMORIA_DESCRIPTIVA","JURISDICTION_CAPABILITY_MATRIX","GOLDEN_THREAD","TECHNICAL_DOSSIER"],"legal_status":"REFERENCE_ONLY","normative_compliance_claimed":False,"native_ifc_file_claimed":False,"construction_approved":False},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# LIGHTHOUSE-000001 Installer v1.4.0\n\nInstala y valida el edificio venezolano documentado: modelo, análisis, dimensionamiento, BIM/IFC neutral, planta, elevación, cuadros estructurales y cantidades coordinadas.\n",encoding="utf-8");(TARGET/"install_lighthouse000001.py").write_text(INSTALLER,encoding="utf-8");(TARGET/"run_lighthouse.py").write_text(RUNNER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_lighthouse_project",r/"src"/"aias_lighthouse_project",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_lighthouse000001_reference_building.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_lighthouse000001_reference_building.py"),"-q"],cwd=r).returncode)
'''
RUNNER='''from pathlib import Path
from aias_lighthouse_project.orchestrator import LighthouseOrchestrator
print(LighthouseOrchestrator().execute(Path("lighthouse000001_outputs").resolve()))
'''
if __name__=="__main__":main()
