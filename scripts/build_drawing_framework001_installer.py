from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_DRAWING_FRAMEWORK001_ENTERPRISE_DRAWING_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for folder in ("src","tests","docs","engineering/aias/drawing_framework","output/pdf"):(PAYLOAD/folder).mkdir(parents=True,exist_ok=True)
 shutil.copytree(ROOT/"src/aias_drawing_framework",PAYLOAD/"src/aias_drawing_framework",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_drawing_framework001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/DRAWING_FRAMEWORK001.md",PAYLOAD/"docs");shutil.copy2(ROOT/"engineering/aias/drawing_framework/DRAWING_STANDARD.json",PAYLOAD/"engineering/aias/drawing_framework")
 for file in (ROOT/"output/pdf").glob("DRW-FOUND-001.*"):shutil.copy2(file,PAYLOAD/"output/pdf")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"AIAS-DRAWING-FRAMEWORK-001","version":"1.0.0","formats":["JSON","SVG","DXF","PDF"],"reference_drawing":"DRW-FOUND-001"},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# DRAWING-FRAMEWORK-001 Installer\n",encoding="utf-8");(TARGET/"install_drawing_framework001.py").write_text(INSTALLER,encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
INSTALLER=r'''import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--project-root",required=True);a=p.parse_args();h=Path(__file__).resolve().parent;r=Path(a.project_root).resolve()
shutil.copytree(h/"payload/src/aias_drawing_framework",r/"src/aias_drawing_framework",dirs_exist_ok=True);shutil.copytree(h/"payload/engineering/aias/drawing_framework",r/"engineering/aias/drawing_framework",dirs_exist_ok=True);shutil.copy2(h/"payload/tests/test_drawing_framework001.py",r/"tests");raise SystemExit(subprocess.run([sys.executable,"-m","pytest",str(r/"tests/test_drawing_framework001.py"),"-q"],cwd=r).returncode)
'''
if __name__=="__main__":main()
