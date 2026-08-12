"""End-to-end Project Lighthouse 001 release orchestration."""
from __future__ import annotations
import hashlib,json,shutil,zipfile
from pathlib import Path
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator
from .brief import reference_brief
from .reporting import descriptive_report
from .traceability import golden_thread
from .validation import validate
from .multistory import execute_reference_design,neutral_bim_ifc_export
from .documentation import generate_structural_documents
class LighthouseOrchestrator:
 """Consume the complete ECP chain and produce a reference-building dossier."""
 def execute(self,workspace:Path)->dict:
  """Generate, validate and package the minimum vertical engineering slice."""
  workspace.mkdir(parents=True,exist_ok=True);upstream=workspace/"upstream";FoundationHandoverOrchestrator().execute(upstream);source=upstream/"source_ecp000001e"/"transmittal";dossier=workspace/"technical_dossier"
  if dossier.exists():shutil.rmtree(dossier)
  shutil.copytree(source/"drawings",dossier/"drawings");shutil.copytree(source/"technical_file",dossier/"technical_file")
  brief=reference_brief();technical=json.loads((dossier/"technical_file"/"foundation_documentation.json").read_text(encoding="utf-8"));files=[p.relative_to(dossier).as_posix() for p in dossier.rglob("*") if p.is_file()];qa=validate(files,brief);thread=golden_thread()
  structural_report=execute_reference_design();bim_export=neutral_bim_ifc_export();documents=generate_structural_documents(dossier/"whole_building_documents",structural_report);capabilities={"profile_id":"VE-001","jurisdiction":"Venezuela","available_reference_capabilities":["three-storey canonical structural model","whole-building reference demand pipeline","reference load combinations and envelopes","batch beam and column sizing","reference optimization","neutral BIM/IFC 4.3 exchange","multiple footings and floor slabs","coordinated structural drawings","beam column and foundation schedules","consolidated quantities","consolidated structural report","foundation calculation","foundation drawings","descriptive report","technical dossier"],"blocked_regulated_capabilities":["Venezuelan normative compliance claim","native IFC certification claim","approved-for-construction release","municipal permit claim"],"activation_dependencies":["licensed and verified Venezuelan normative pack","site-specific inputs","independent benchmark acceptance","qualified professional approval"]}
  (dossier/"PROJECT_BRIEF.json").write_text(json.dumps(brief,indent=2)+"\n",encoding="utf-8");(dossier/"WHOLE_BUILDING_STRUCTURAL_REPORT.json").write_text(json.dumps(structural_report,indent=2)+"\n",encoding="utf-8");(dossier/"REFERENCE_LOAD_COMBINATIONS.json").write_text(json.dumps(structural_report["reference_load_envelopes"],indent=2)+"\n",encoding="utf-8");(dossier/"WHOLE_BUILDING_BIM_IFC_NEUTRAL.json").write_text(json.dumps(bim_export,indent=2)+"\n",encoding="utf-8");(dossier/"WHOLE_BUILDING_DOCUMENTATION_SUMMARY.json").write_text(json.dumps(documents,indent=2)+"\n",encoding="utf-8");(dossier/"JURISDICTION_CAPABILITY_MATRIX.json").write_text(json.dumps(capabilities,indent=2)+"\n",encoding="utf-8");(dossier/"GOLDEN_THREAD.json").write_text(json.dumps(thread,indent=2)+"\n",encoding="utf-8");(dossier/"VALIDATION.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8");(dossier/"MEMORIA_DESCRIPTIVA.md").write_text(descriptive_report(brief,technical),encoding="utf-8")
  if not qa["complete"] or not qa["safe_reference_status"]:raise ValueError(qa)
  release=workspace/"release";release.mkdir(exist_ok=True);archive=release/"LIGHTHOUSE-000001_VENEZUELA_DOCUMENTED_BUILDING_1.4.0.zip"
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
   for path in sorted(dossier.rglob("*")):
    if path.is_file():bundle.write(path,path.relative_to(dossier))
  digest=hashlib.sha256(archive.read_bytes()).hexdigest();(release/f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n",encoding="utf-8")
  return {"validated":True,"project_id":brief["project_id"],"legal_status":brief["legal_status"],"construction_approved":False,"artifacts":len([p for p in dossier.rglob("*") if p.is_file()]),"reference_capability_level":qa["reference_capability_level"],"archive":str(archive),"sha256":digest}
