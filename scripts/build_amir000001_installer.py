from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_AMIR000001_MASTER_INVENTORY_ROADMAP_INSTALLER";PAYLOAD=TARGET/"payload"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_master_inventory",PAYLOAD/"src"/"aias_master_inventory",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_amir000001_master_inventory.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"AMIR000001_MASTER_INVENTORY.md",PAYLOAD/"docs")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-AMIR-000001","version":"1.0.0","concepts":63,"waves":22,"outputs":["MASTER_INVENTORY","MATERIALIZATION_ROADMAP","LIGHTHOUSE_CONTRACT","RELEASE_ZIP"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# AMIR-000001 Installer\n\nInstala y valida el inventario maestro y la hoja de ruta.\n",encoding="utf-8");(TARGET/"install_amir000001.py").write_text(INSTALLER,encoding="utf-8");(TARGET/"run_inventory.py").write_text(RUNNER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{digest(p)}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_master_inventory",r/"src"/"aias_master_inventory",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_amir000001_master_inventory.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_amir000001_master_inventory.py"),"-q"],cwd=r).returncode)
'''
RUNNER='''from pathlib import Path
from aias_master_inventory.orchestrator import MasterInventoryOrchestrator
print(MasterInventoryOrchestrator().execute(Path(".").resolve(),Path("engineering/aias/master/inventory").resolve()))
'''
if __name__=="__main__":main()
