from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_DEV_PLATFORM001_UNIFIED_DEVELOPMENT_PLATFORM_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/development_platform"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 for package in ("aias_development_platform","aias_aeps_automation_v3","aias_aeps_advanced_v4","aias_aeps_autonomous_v5"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_dev_platform001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/DEV_PLATFORM001_UNIFIED_DEVELOPMENT_PLATFORM.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/development_platform/DEVELOPMENT_PLATFORM_POLICY.json",PAYLOAD/"engineering/aias/development_platform")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-DEV-PLATFORM-001","version":"1.0.0","engines":["AEPS-V3","AEPS-V4","AEPS-V5"],"outputs":["UNIFIED_CONTRACT","GOVERNED_SELECTION","ISOLATED_EXECUTION","NORMALIZED_EVIDENCE","LIFECYCLE_EVENTS"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# DEV-PLATFORM-001 Installer\n",encoding="utf-8");(TARGET/"install_dev_platform001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload/src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering/aias/development_platform",r/"engineering/aias/development_platform",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_dev_platform001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_dev_platform001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
