import json
from datetime import date
from pathlib import Path
import pytest
from aias_engineering_wave12 import *
ROOT=Path(__file__).resolve().parents[1]
def pack():return JurisdictionPack(**{k:tuple(v) if k=="rules" else v for k,v in json.loads((ROOT/"engineering/aias/engineering_wave12/REFERENCE_JURISDICTION_PACK.json").read_text()).items()})
def test_jurisdiction_reference_requires_explicit_opt_in():
 r=JurisdictionRegistry();r.register(pack())
 with pytest.raises(ValueError,match="explicit_opt_in"):r.resolve("JUR-DEMO-001",date(2026,8,3))
 assert r.resolve("JUR-DEMO-001",date(2026,8,3),True).legal_status=="REFERENCE_ONLY"
def test_evidence_ledger_is_hash_chained_and_detects_tampering(tmp_path):
 ledger=EngineeringEvidenceLedger(tmp_path/"ledger.json");ledger.append("E1","CALC","engine",{"value":1});ledger.append("E2","CHECK","engine",{"passed":True});assert ledger.verify()["valid"]
 ledger.data["records"][0]["payload"]["value"]=2;assert not ledger.verify()["valid"]
def test_differential_validation_is_unit_and_provenance_aware():
 baseline={"values":{"q":160.0},"units":{"q":"kPa"},"provenance":"REF"};candidate={"values":{"q":160.01},"units":{"q":"kPa"},"provenance":"RUN"};assert DifferentialValidator().compare(baseline,candidate,.001,.001)["passed"]
 with pytest.raises(ValueError,match="unit_mismatch"):DifferentialValidator().compare(baseline,{**candidate,"units":{"q":"Pa"}},.1,.1)
def test_project_reference_library_requires_anonymized_licensed_case():
 case=json.loads((ROOT/"engineering/aias/engineering_wave12/REFERENCE_PROJECT_CASE.json").read_text());row=ProjectReferenceLibrary().register(case);assert len(row["case_sha256"])==64
def test_foundation_professional_workflow_is_immediate_real_consumer(tmp_path):
 result=FoundationProfessionalWorkflow().execute(tmp_path/"professional");assert result["validated"] and result["ledger"]["records"]==2 and result["professional_review_required"]
