from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_WORKSPACE2_W2_03_BIM_INSPECTOR_INSTALLER"
PAYLOAD = TARGET / "payload"


def main():
    if TARGET.exists(): shutil.rmtree(TARGET)
    sources = ("src/gui/workspace2", "engineering/aias/experience/AIAS_WORKSPACE2_W2_03_SPEC.json", "docs/AIAS_WORKSPACE2_W2_03.md", "tests/test_aias_workspace2_w2_03.py")
    for relative in sources:
        source, destination = ROOT / relative, PAYLOAD / relative; destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir(): shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else: shutil.copy2(source, destination)
    (TARGET / "manifest.json").write_text(json.dumps({"pack_id":"AIAS-WORKSPACE-2.0-W2-03","version":"0.3.0","status":"IMPLEMENTED_VALIDATED","next":"W2-04"}, indent=2)+"\n", encoding="utf-8")
    files=sorted(path for path in TARGET.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(TARGET).as_posix()}" for path in files)+"\n", encoding="utf-8")
    print(json.dumps({"target":str(TARGET),"files":len(files)}))


if __name__ == "__main__": main()
