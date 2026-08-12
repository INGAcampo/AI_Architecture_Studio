from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_WORKSPACE2_FOUNDATION_INSTALLER"
PAYLOAD = TARGET / "payload"


def main():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    for source, relative in (
        (ROOT / "src/gui/workspace2", "src/gui/workspace2"),
        (ROOT / "src/gui/main_window.py", "src/gui/main_window.py"),
        (ROOT / "engineering/aias/experience/AIAS_WORKSPACE2_FOUNDATION_SPEC.json", "engineering/aias/experience/AIAS_WORKSPACE2_FOUNDATION_SPEC.json"),
        (ROOT / "tests/test_aias_workspace2_foundation.py", "tests/test_aias_workspace2_foundation.py"),
    ):
        destination = PAYLOAD / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(source, destination)
    manifest = {"pack_id": "AIAS-WORKSPACE-2.0-FOUNDATION", "version": "0.1.0", "increment": "W2-01", "status": "IMPLEMENTED_RENDERED_VALIDATION_PENDING", "next": "W2-02"}
    (TARGET / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files = sorted(path for path in TARGET.rglob("*") if path.is_file() and path.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(TARGET).as_posix()}" for path in files) + "\n", encoding="utf-8")
    print(json.dumps({"target": str(TARGET), "files": len(files)}))


if __name__ == "__main__":
    main()
