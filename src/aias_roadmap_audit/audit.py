from __future__ import annotations
import hashlib,json
from pathlib import Path

EVIDENCE={
 "G1":["src/aias_structural_codes_program/building.py","src/aias_structural_codes_program/analysis.py","src/aias_structural_codes_program/design.py","src/aias_structural_codes_program/reporting.py"],
 "G2":["src/aias_structural_codes_program/normative.py","src/aias_structural_codes_program/material_codes.py"],
 "G3":["src/aias_structural_codes_program/benchmarking.py","src/aias_structural_codes_program/release.py"],
 "G4":["src/aias_cad_bim_integration/ifc_sync.py","src/aias_structural_codes_program/int02.py","src/aias_cad_bim_integration/design_adapters.py"],
 "G5":["src/aias_structural_codes_program/geo01.py","src/aias_structural_codes_program/geo02.py"],
 "G6":["src/aias_structural_codes_program/mdp02.py","src/aias_structural_codes_program/mdp03.py","src/aias_structural_codes_program/hyd01.py"],
 "G7":["src/aias_engineering_intelligence","src/aias_structural_codes_program/plt01.py"],
 "G8":["src/aias_productivity_dashboard","src/aias_structural_codes_program/coord01.py","src/aias_documentation_program"],
 "G9":["src/aias_structural_codes_program/plt01.py","src/aias_security_recovery","src/aias_level5_assurance"],
}
EXTERNAL_GATES={"G2":"licensed jurisdictional standards","G3":"independent professional benchmark acceptance","G4":"licensed vendor runtimes and production APIs","G9":"longitudinal production evidence and independent maturity audit"}
class IntegralRoadmapAuditor:
 def audit(self,root:Path)->dict:
  root=root.resolve();issues=[];waves=json.loads((root/"engineering/aias/master/inventory/AIAS_MATERIALIZATION_ROADMAP.json").read_text(encoding="utf-8"))["waves"];structural=json.loads((root/"engineering/aias/structural_codes/STRUCTURAL_PLATFORM_ROADMAP.json").read_text(encoding="utf-8"));giant=json.loads((root/"engineering/aias/master/GIANT_STEPS_WORK_PLAN.json").read_text(encoding="utf-8"))
  material=[x for wave in waves for x in wave["items"]];pending=[x for x in material if x["state"] not in {"OPERATIONAL","SPECIFIED"}];specified=[x for x in material if x["state"]=="SPECIFIED"]
  stages=structural["stages"];stage_pending=[x for x in stages if not x["status"].startswith("IMPLEMENTED")]
  macro=[]
  for item in giant["macrodeliveries"]:
   missing=[p for p in EVIDENCE[item["id"]] if not (root/p).exists()];status="TECHNICALLY_EVIDENCED" if not missing else "MISSING_EVIDENCE"
   if missing:issues.append(f"{item['id']}:missing:{missing}")
   macro.append({"id":item["id"],"title":item["title"],"status":status,"evidence":EVIDENCE[item["id"]],"external_gate":EXTERNAL_GATES.get(item["id"])})
  installers=[]
  for manifest in sorted(root.glob("AIAS_*_INSTALLER/checksums.sha256")):
   errors=[]
   for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line.strip():continue
    expected,relative=line.split("  ",1);target=manifest.parent/relative
    if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=expected:errors.append(relative)
   installers.append({"installer":manifest.parent.name,"entries":len(manifest.read_text(encoding="utf-8").splitlines()),"valid":not errors,"errors":errors})
  if pending:issues.append("materialization_pending")
  if stage_pending:issues.append("structural_stages_pending")
  if any(not x["valid"] for x in installers):issues.append("installer_integrity_failure")
  payload={"audit_id":"ROADMAP-AUDIT-001","materialization":{"total":len(material),"operational":sum(x["state"]=="OPERATIONAL" for x in material),"specified":specified,"pending":pending},"structural":{"total":len(stages),"implemented":len(stages)-len(stage_pending),"pending":stage_pending},"giant_steps":macro,"installers":{"count":len(installers),"entries":sum(x["entries"] for x in installers),"all_valid":all(x["valid"] for x in installers)},"technical_issues":issues,"external_gates":[{"macrodelivery":key,"condition":value} for key,value in EXTERNAL_GATES.items()]}
  payload["technical_macrodeliveries_complete"]=not issues;payload["audit_sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();return payload
 def write(self,root:Path,output:Path):
  result=self.audit(root);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return result
