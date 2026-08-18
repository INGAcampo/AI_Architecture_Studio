from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_GOV_CONTINUITY001_VERIFIABLE_HANDOFF_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","engineering/aeps/02_CONSTITUTION","engineering/aias/master"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_context_engine",PAYLOAD/"src/aias_context_engine",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
 shutil.copy2(ROOT/"tests/test_aec000051_continuity_rule.py",PAYLOAD/"tests");shutil.copy2(ROOT/"engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml",PAYLOAD/"engineering/aeps/02_CONSTITUTION");shutil.copy2(ROOT/"engineering/aias/master/CONVERSATION_CONTINUITY_POLICY.json",PAYLOAD/"engineering/aias/master")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-GOV-CONTINUITY-001","article":"AEC-000051","version":"1.0.1","payload_layout":"payload/src/aias_context_engine","outputs":["VERIFIED_HANDOFF","SHA256_MANIFEST","ACE_CLI","CONTINUITY_POLICY"]},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# GOV-CONTINUITY-001 Installer v1.0.1\n\nInstalls the complete package under `src/aias_context_engine`; it never creates flattened modules in `src`.\n",encoding="utf-8");(TARGET/"install_gov_continuity001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,os,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve();shutil.copytree(h/"payload/src/aias_context_engine",r/"src/aias_context_engine",dirs_exist_ok=True)
shutil.copytree(h/"payload/engineering",r/"engineering",dirs_exist_ok=True);(r/"tests").mkdir(parents=True,exist_ok=True);shutil.copy2(h/"payload/tests/test_aec000051_continuity_rule.py",r/"tests")
env=dict(os.environ);env["PYTHONPATH"]=str(r/"src")+os.pathsep+env.get("PYTHONPATH","");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_aec000051_continuity_rule.py"),"-q"],cwd=r,env=env).returncode)
'''
if __name__=="__main__":main()
