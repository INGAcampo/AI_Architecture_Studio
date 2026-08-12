from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_ASSET_REGISTRY001_UNIVERSAL_REGISTRY_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs","engineering/aias/foundation"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_asset_registry",PAYLOAD/"src"/"aias_asset_registry",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_asset_registry001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"ASSET_REGISTRY001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering"/"aias"/"foundation"/"ENGINEERING_ASSET_SCHEMA.json",PAYLOAD/"engineering"/"aias"/"foundation")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-ASSET-REGISTRY-001","version":"1.0.0","outputs":["ASSET_SCHEMA","PERSISTENT_REGISTRY","AUDIT_EVENTS"]},indent=2)+"\n",encoding="utf-8");(TARGET/"install_asset_registry001.py").write_text(INSTALLER,encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# ASSET-REGISTRY-001 Installer\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(TARGET)
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_asset_registry",r/"src"/"aias_asset_registry",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_asset_registry001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_asset_registry001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
