from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_CNS000001_CENTRAL_NERVOUS_SYSTEM_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs","engineering/aias/cns"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src"/"aias_central_nervous_system",PAYLOAD/"src"/"aias_central_nervous_system",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests"/"test_cns000001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"CNS000001_CENTRAL_NERVOUS_SYSTEM.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering"/"aias"/"cns"/"AIAS_CNS_TOPOLOGY.json",PAYLOAD/"engineering"/"aias"/"cns")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-CNS-000001","version":"1.0.0","outputs":["CNS_TOPOLOGY","IMMUTABLE_EVENTS","ATOMIC_JOURNAL","CONSUMER_CURSORS","DEAD_LETTERS","COMPANY_STATE_PROJECTION"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# CNS-000001 Installer\n",encoding="utf-8");(TARGET/"install_cns000001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload"/"src"/"aias_central_nervous_system",r/"src"/"aias_central_nervous_system",dirs_exist_ok=True);shutil.copytree(h/"payload"/"engineering"/"aias"/"cns",r/"engineering"/"aias"/"cns",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_cns000001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_cns000001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
