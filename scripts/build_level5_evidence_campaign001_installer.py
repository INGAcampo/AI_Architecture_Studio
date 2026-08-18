from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_LEVEL5_EVIDENCE_CAMPAIGN001_LONGITUDINAL_LEDGER_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/roadmap"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_level5_assurance",PAYLOAD/"src/aias_level5_assurance",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_level5_evidence_campaign001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/LEVEL5_EVIDENCE_CAMPAIGN001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/roadmap/LEVEL5_EVIDENCE_CAMPAIGN.json",PAYLOAD/"engineering/aias/roadmap")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-LEVEL5-EVIDENCE-CAMPAIGN-001","version":"1.0.0","production_key_embedded":False,"status":"ACTIVE_EVIDENCE_COLLECTION","outputs":["AUTHENTICATED_LEDGER","HASH_CHAIN","CAMPAIGN_STATUS","ASSESSOR_PROJECTION","CLI"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# LEVEL5-EVIDENCE-CAMPAIGN-001 Installer\n\nRequires an externally managed signing key of at least 32 bytes.\n",encoding="utf-8");(TARGET/"install_level5_evidence_campaign001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_level5_assurance",r/"src/aias_level5_assurance",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/roadmap",r/"engineering/aias/roadmap",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_level5_evidence_campaign001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_level5_evidence_campaign001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
