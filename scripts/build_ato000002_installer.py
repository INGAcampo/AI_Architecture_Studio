from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_ATO000002_CONTINUOUS_OBSERVATORY_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for f in ("src","tests","docs","engineering/aias/ato"):(PAYLOAD/f).mkdir(parents=True,exist_ok=True)
 for package in ("aias_continuous_observatory","aias_technology_observatory"):shutil.copytree(ROOT/"src"/package,PAYLOAD/"src"/package,ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests"/"test_ato000002_continuous_observatory.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs"/"ATO000002_CONTINUOUS_OBSERVATORY.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering"/"aias"/"ato"/"ATO_CONTINUOUS_SOURCE_REGISTRY.json",PAYLOAD/"engineering"/"aias"/"ato")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-ATO-000002","version":"1.0.0","outputs":["AUTHORIZED_SOURCE_REGISTRY","CONTINUOUS_CYCLE","TECHNOLOGY_RADAR","AEC_000050_RECOMMENDATIONS","PERSISTENT_LEDGER"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# ATO-000002 Installer\n\nInstala el observatorio continuo y ejecuta sus pruebas deterministas.\n",encoding="utf-8");(TARGET/"install_ato000002.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
for package in (h/"payload"/"src").glob("aias_*"):shutil.copytree(package,r/"src"/package.name,dirs_exist_ok=True)
shutil.copytree(h/"payload"/"engineering"/"aias"/"ato",r/"engineering"/"aias"/"ato",dirs_exist_ok=True);shutil.copy2(h/"payload"/"tests"/"test_ato000002_continuous_observatory.py",r/"tests")
raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests"/"test_ato000002_continuous_observatory.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
