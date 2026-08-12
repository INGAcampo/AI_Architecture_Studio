"""Generate the governed AIAS IMS foundation reference evidence."""
from __future__ import annotations
import json,shutil
from pathlib import Path
from aias_integrated_management import CorrectiveAction,IntegratedManagementSystem,ManagementObjective,ManagementRisk
ROOT=Path(__file__).resolve().parents[1];OUTPUT=ROOT/"engineering/aias/certification/ims"
def main():
 if OUTPUT.exists():shutil.rmtree(OUTPUT)
 ims=IntegratedManagementSystem(OUTPUT);ims.initialize()
 risks=(
  ManagementRisk("IMSR-001","QUALITY","Untraced requirement affects an engineering deliverable",2,5,"Quality Office","Enforce SDD traceability gates"),
  ManagementRisk("IMSR-002","INFORMATION_SECURITY","Evidence loses confidentiality, integrity or availability",3,5,"Security Office","Apply access, integrity and recovery controls"),
  ManagementRisk("IMSR-003","AI_MANAGEMENT","AI recommendation bypasses accountable professional review",3,5,"AI Office","Enforce human maker-checker and final-authority boundaries"),
  ManagementRisk("IMSR-004","BUSINESS_CONTINUITY","Critical engineering service cannot recover within its objective",3,5,"Security Office","Maintain tested backups and recovery exercises"),)
 for row in risks:ims.add_risk(row)
 objectives=(
  ManagementObjective("IMSO-001","QUALITY","Maintain governed requirements traceability","traceability_coverage",0.0,.95,"2027-08-03","Quality Office"),
  ManagementObjective("IMSO-002","INFORMATION_SECURITY","Verify recoverability of governed evidence","verified_recovery_rate",0.0,.95,"2027-08-03","Security Office"),
  ManagementObjective("IMSO-003","AI_MANAGEMENT","Require professional review for regulated AI-assisted outputs","professional_review_compliance",0.0,1.0,"2027-08-03","AI Office"),
  ManagementObjective("IMSO-004","BUSINESS_CONTINUITY","Exercise critical-service recovery plans","continuity_exercise_completion",0.0,1.0,"2027-08-03","Security Office"),)
 for row in objectives:ims.add_objective(row)
 ims.schedule_internal_audit("IMS-AUD-001",("QUALITY","INFORMATION_SECURITY","AI_MANAGEMENT","BUSINESS_CONTINUITY"),"2026-11-03T00:00:00+00:00","AIAS Independent Internal Audit Function")
 ims.record_management_review("IMS-MR-001",{"certification_master_plan":"VALIDATED","external_certification":False,"normative_copies":"REQUIRED_FOR_CLAUSE_CROSSWALK"},("Fund legitimate normative access","Execute internal audit program","Retain external certification authority"),"2026-08-03T00:00:00+00:00")
 ims.add_corrective_action(CorrectiveAction("IMSCA-001","CERTIFICATION-MASTER-PLAN-001","Clause-level crosswalk unavailable","Licensed normative texts not yet acquired","Acquire legitimate normative access and confirm certification scope","Compliance Office","2026-12-31"))
 readiness=ims.readiness();(OUTPUT/"IMS_READINESS.json").write_text(json.dumps(readiness,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print({"output":str(OUTPUT),"readiness":readiness})
if __name__=="__main__":main()
