from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_SECURITY_RECOVERY001_VERIFIABLE_RECOVERY_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/security_recovery"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_security_recovery",PAYLOAD/"src/aias_security_recovery",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_security_recovery001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/SECURITY_RECOVERY001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/security_recovery/SECURITY_RECOVERY_POLICY.json",PAYLOAD/"engineering/aias/security_recovery")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-SECURITY-RECOVERY-001","version":"1.0.0","outputs":["SECRET_EXCLUSION","SIGNED_SNAPSHOT","INTEGRITY_VERIFICATION","SAFE_RESTORE","RECOVERY_DRILL","RPO_RTO_EVIDENCE","RETENTION_PLAN"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# SECURITY-RECOVERY-001 Installer\n",encoding="utf-8");(TARGET/"install_security_recovery001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_security_recovery",r/"src/aias_security_recovery",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/security_recovery",r/"engineering/aias/security_recovery",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_security_recovery001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_security_recovery001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
