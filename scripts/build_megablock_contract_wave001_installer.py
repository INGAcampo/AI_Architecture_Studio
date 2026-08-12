from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "AIAS_MEGABLOCK_CONTRACT_WAVE001_INSTALLER"
def main() -> None:
    if TARGET.exists(): shutil.rmtree(TARGET)
    payload = TARGET / "payload"
    for rel in ("engineering/aias/roadmap/MEGABLOCK_CONTRACT_WAVE_001.json", "engineering/megablock_contract_wave001", "docs/MEGABLOCK_CONTRACT_WAVE_001.md", "tests/test_megablock_contract_wave001.py"):
        src, dst = ROOT / rel, payload / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)
    (TARGET / "manifest.json").write_text(json.dumps({"pack_id":"MEGABLOCK-CONTRACT-WAVE-001","version":"1.0.0","status":"SPECIFICATION_GATE","external_evidence_required":True}, indent=2) + "\n", encoding="utf-8")
    files = sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name != "checksums.sha256")
    (TARGET / "checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files) + "\n", encoding="utf-8")
    print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__ == "__main__": main()
