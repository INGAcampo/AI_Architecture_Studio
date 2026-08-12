from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_CAD_BIM_INTEGRATION001_CANONICAL_BRIDGE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/cad_bim_integration"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 for package in ("aias_cad_bim_integration","aias_drawing_framework"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_cad_bim_integration001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_bim_ifc_neutral_sync_int01.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_design_application_adapters_int03.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/CAD_BIM_INTEGRATION001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/cad_bim_integration/INTERCHANGE_CONTRACT.json",PAYLOAD/"engineering/aias/cad_bim_integration")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-CAD-BIM-INTEGRATION-001","version":"1.2.0","outputs":["NEUTRAL_INTERCHANGE","BIM_DRAWING_PROJECTION","LOSS_REPORT","INTEGRITY_ROUNDTRIP","ALLOWLISTED_SYNC","IFC43_NEUTRAL_SYNC","CONFLICT_DETECTION","AUTOCAD_REVIT_CIVIL3D_GATES"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# CAD-BIM-INTEGRATION-001 Installer v1.2.0\n",encoding="utf-8");(TARGET/"install_cad_bim_integration001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,os,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload/src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering/aias/cad_bim_integration",r/"engineering/aias/cad_bim_integration",dirs_exist_ok=True);(r/"tests").mkdir(parents=True,exist_ok=True)
for name in ("test_cad_bim_integration001.py","test_bim_ifc_neutral_sync_int01.py","test_design_application_adapters_int03.py"):shutil.copy2(h/"payload/tests"/name,r/"tests"/name)
env=dict(os.environ);env["PYTHONPATH"]=str(r/"src")+os.pathsep+env.get("PYTHONPATH","");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_cad_bim_integration001.py"),str(r/"tests/test_bim_ifc_neutral_sync_int01.py"),str(r/"tests/test_design_application_adapters_int03.py"),"-q"],cwd=r,env=env).returncode)
'''
if __name__=="__main__":main()
