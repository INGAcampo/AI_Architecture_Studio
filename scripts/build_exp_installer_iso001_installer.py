from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_EXP_INSTALLER_ISO001_DISTRIBUTION_FOUNDATION_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 for relative in ("src/aias_distribution","engineering/aias/experience/EXP_INSTALLER_ISO_001_SPEC.json","docs/EXP_INSTALLER_ISO_001.md","tests/test_exp_installer_iso001.py","scripts/build_exp_installer_iso001_media.py","exp_installer_iso001_outputs/OFFLINE_MEDIA_BUILD_REPORT.json"):
  source,destination=ROOT/relative,PAYLOAD/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(source,destination,ignore=shutil.ignore_patterns("__pycache__","*.pyc")) if source.is_dir() else shutil.copy2(source,destination)
 media=ROOT/"exp_installer_iso001_outputs/AIAS_INTERNAL_OFFLINE_MEDIA_1.0.0.zip";shutil.copy2(media,TARGET/media.name)
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"EXP-INSTALLER-ISO-001","version":"1.0.0","status":"INTEGRITY_VALIDATED_UNSIGNED_INTERNAL_MEDIA","publisher_signed":False,"iso_image_created":False,"next":"EXP-WEB-001"},indent=2)+"\n",encoding="utf-8");files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print(json.dumps({"target":str(TARGET),"files":len(files)}))
if __name__=="__main__":main()
