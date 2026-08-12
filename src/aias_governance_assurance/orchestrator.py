"""Generate canonical governance, documentation and SDD assurance evidence."""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from .decisions import registry
from .documentation import audit as documentation_audit
from .sdd import audit_compliance

class GovernanceAssuranceOrchestrator:
 """Materialize recovered governance decisions into auditable artifacts."""
 def execute(self,root:Path,output:Path)->dict:
  """Audit ``root`` and write the canonical assurance package to ``output``."""
  output.mkdir(parents=True,exist_ok=True);decisions=registry();docs=documentation_audit(root);sdd=audit_compliance(root)
  for row in decisions:row["materialized"]=(root/row["evidence"]).exists()
  binding=[r for r in decisions if r["classification"]=="BINDING"]
  matrix={"generated_at":datetime.now(timezone.utc).isoformat(),"source":"Captura de pantalla (6).zip, captures 1700-2588","decisions":decisions,"binding_materialization_coverage":sum(r["materialized"] for r in binding)/len(binding)}
  backlog=[]
  if not docs["complete"]:backlog.append({"priority":"P0","id":"DOC-ALIGN-001","action":"Document undocumented modules and public symbols progressively, prioritizing active engineering packages.","count":len(docs["missing"])})
  if not sdd["all_complete"]:backlog.append({"priority":"P0","id":"SDD-ALIGN-001","action":"Generate compliance packs for legacy components without retroactively claiming validation.","count":sdd["component_count"]-sdd["complete_count"]})
  certification_plan=(root/"engineering/aias/certification/AIAS_CERTIFICATION_MASTER_PLAN.json").is_file()
  ims_foundation=(root/"engineering/aias/certification/IMS_FOUNDATION_POLICY.json").is_file()
  normative_access=(root/"engineering/aias/certification/NORMATIVE_ACCESS_PLAN.json").is_file()
  current="GOV-000049 Historical Decision Materialization and SDD Assurance" if backlog else ("CERTIFICATION-NORMATIVE-ACCESS-001 Procurement Readiness - VALIDATED" if normative_access else ("CERTIFICATION-IMS-FOUNDATION-001 Integrated Management System - VALIDATED" if ims_foundation else ("CERTIFICATION-MASTER-PLAN-001 Official Framework Decision - VALIDATED" if certification_plan else "ROADMAP-COMPLETION-AUDIT Technical Macrodeliveries - COMPLETE")))
  next_item="Documentation and legacy-SDD alignment backlog" if backlog else ("CERTIFICATION-EXTERNAL-SELECTION-001 Provider, Budget and Contract Authorization - EXTERNAL DECISION" if normative_access else ("CERTIFICATION-NORMATIVE-ACCESS-001 Licensed Standards and External Gap Assessment - NEXT" if ims_foundation else ("CERTIFICATION-IMS-FOUNDATION-001 Integrated Management System - NEXT" if certification_plan else "LEVEL5-EVIDENCE-CAMPAIGN-001 Longitudinal Maturity Evidence - ACTIVE")))
  master={"plan_id":"AMDP-000001","version":"1.0.0","status":"ACTIVE","governing_rules":["AEC-000024","AEC-000049","ASDD-000002"],"current":current,"next":next_item,"metrics":{"binding_decisions":len(binding),"materialized_binding_decisions":sum(r["materialized"] for r in binding),"documentation_module_coverage":docs["module_coverage"],"documentation_public_symbol_coverage":docs["public_symbol_coverage"],"sdd_compliant_components":sdd["complete_count"]},"backlog":backlog}
  artifacts={"HISTORICAL_DECISION_MATRIX.json":matrix,"DOCUMENTATION_COVERAGE.json":docs,"SDD_ASSURANCE.json":sdd,"AIAS_MASTER_DEVELOPMENT_PLAN.json":master,"ALIGNMENT_BACKLOG.json":backlog}
  for name,data in artifacts.items():(output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  lines=["# AIAS Historical Decision Materialization Matrix","",f"Source: `{matrix['source']}`","","| ID | Captures | Class | Materialized | Decision |","|---|---|---|---:|---|"]
  lines += [f"| {r['decision_id']} | {r['captures']} | {r['classification']} | {'YES' if r['materialized'] else 'NO'} | {r['decision']} |" for r in decisions]
  (output/"HISTORICAL_DECISION_MATRIX.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
  digest=hashlib.sha256(json.dumps(artifacts,sort_keys=True,ensure_ascii=False).encode()).hexdigest();(output/"ASSURANCE.sha256").write_text(digest+"\n",encoding="utf-8")
  return {"validated":True,"decisions":len(decisions),"binding_coverage":matrix["binding_materialization_coverage"],"module_doc_coverage":docs["module_coverage"],"symbol_doc_coverage":docs["public_symbol_coverage"],"sdd_components":sdd["component_count"],"alignment_items":len(backlog),"sha256":digest}
