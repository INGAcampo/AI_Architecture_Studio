from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_ADF002_DEPENDENCY_GRAPH_INSTALLER"

def main() -> None:
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload = TARGET / "payload"
    for rel in ("src/aias_adf2", "engineering/aias/development_factory/ADF_002_DEPENDENCY_GRAPH.json", "engineering/adf002/compliance", "docs/ADF_002.md", "tests/test_adf002_dependency_graph.py"):
        source, dest = ROOT / rel, payload / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")) if source.is_dir() else shutil.copy2(source, dest)
    (TARGET / "manifest.json").write_text(json.dumps({"pack_id":"ADF-002","version":"1.0.0","status":"CONFORMANT","next":"MEGABLOCK-GEOMETRY-2 / MEGABLOCK-BIM-NATIVE-2 / MEGABLOCK-STRUCTURAL-1"}, indent=2) + "\n", encoding="utf-8")
    files = sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files) + "\n", encoding="utf-8")
    print(json.dumps({"target": str(TARGET), "files": len(files)}))

if __name__ == "__main__": main()
