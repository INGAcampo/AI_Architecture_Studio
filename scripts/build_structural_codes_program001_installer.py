from __future__ import annotations
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TARGET=ROOT/"AIAS_STRUCTURAL_CODES_PROGRAM001_LIVING_KNOWLEDGE_INSTALLER";PAYLOAD=TARGET/"payload"
def main():
 if TARGET.exists():shutil.rmtree(TARGET)
 (PAYLOAD/"src").mkdir(parents=True);(PAYLOAD/"tests").mkdir();(PAYLOAD/"docs").mkdir();(PAYLOAD/"engineering/aias/structural_codes").mkdir(parents=True)
 shutil.copytree(ROOT/"src/aias_structural_codes_program",PAYLOAD/"src/aias_structural_codes_program",ignore=shutil.ignore_patterns("__pycache__","*.pyc"));shutil.copy2(ROOT/"tests/test_structural_codes_program001.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_structural_benchmarking_scp08.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_structural_release_scp09.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_multidisciplinary_mdp01.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_ground_water_engineering_mdp02.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_civil_spatial_infrastructure_mdp03.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_soil_structure_interaction_geo01.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_deep_foundations_geo02.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_hydraulic_networks_hyd01.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_vendor_adapters_int02.py",PAYLOAD/"tests");shutil.copy2(ROOT/"tests/test_platform_acceleration_plt01.py",PAYLOAD/"tests");shutil.copy2(ROOT/"docs/STRUCTURAL_CODES_PROGRAM001.md",PAYLOAD/"docs");shutil.copytree(ROOT/"engineering/aias/structural_codes",PAYLOAD/"engineering/aias/structural_codes",dirs_exist_ok=True)
 shutil.copy2(ROOT/"tests/test_coordination_dashboard_coord01.py",PAYLOAD/"tests")
 shutil.copy2(ROOT/"tests/test_venezuela_jurisdiction_profile.py",PAYLOAD/"tests")
 shutil.copy2(ROOT/"docs/VENEZUELA_NORMATIVE_CATALOG_INQUIRY.md",PAYLOAD/"docs")
 (PAYLOAD/"docs/outbound").mkdir()
 shutil.copy2(ROOT/"docs/outbound/VE-002_FONDONORMA_CATALOG_INQUIRY.eml",PAYLOAD/"docs/outbound")
 (TARGET/"manifest.json").write_text(json.dumps({"pack_id":"STRUCTURAL-CODES-PROGRAM-001","version":"2.2.0","status":"VENEZUELA_INITIAL_JURISDICTION_SELECTED","normative_codes_claimed":False,"construction_approval_claimed":False},indent=2)+"\n",encoding="utf-8");(TARGET/"README_INSTALACION.md").write_text("# STRUCTURAL-CODES-PROGRAM-001 v2.2.0\n\nIncludes the formally selected Venezuela initial-jurisdiction profile. Normative calculation remains gated by official edition verification, licensed acquisition, executable-rule validation, independent benchmarks and professional approval.\n",encoding="utf-8")
 files=sorted(p for p in TARGET.rglob("*") if p.is_file() and p.name!="checksums.sha256");(TARGET/"checksums.sha256").write_text("\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(TARGET).as_posix()}" for p in files)+"\n",encoding="utf-8");print({"target":str(TARGET),"files":len(files)})
if __name__=="__main__":main()
