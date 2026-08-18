from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_CERTIFICATION_IMS_FOUNDATION001_INTEGRATED_SYSTEM_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/certification"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_integrated_management",PAYLOAD/"src/aias_integrated_management",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_certification_ims_foundation001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/CERTIFICATION_IMS_FOUNDATION001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/certification/IMS_FOUNDATION_POLICY.json",PAYLOAD/"engineering/aias/certification");shutil.copytree(ROOT/"engineering/aias/certification/ims",PAYLOAD/"engineering/aias/certification/ims",dirs_exist_ok=True)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-CERTIFICATION-IMS-FOUNDATION-001","version":"1.0.0","status":"IMPLEMENTED_FOUNDATION_NOT_CERTIFIED","framework_targets":["ISO-9001","ISO-IEC-27001","ISO-IEC-42001","ISO-22301"],"external_certification_claim":False},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# CERTIFICATION-IMS-FOUNDATION-001 Installer\n",encoding="utf-8");(TARGET/"install_certification_ims_foundation001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload/src/aias_integrated_management",r/"src/aias_integrated_management",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/certification",r/"engineering/aias/certification",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_certification_ims_foundation001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_certification_ims_foundation001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
