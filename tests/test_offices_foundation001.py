from pathlib import Path
import pytest
from aias_enterprise_offices import OfficeRegistry,WorkItem
from aias_enterprise_offices.bootstrap import load_charters
ROOT=Path(__file__).resolve().parents[1];CHARTERS=ROOT/"engineering/aias/offices/ENTERPRISE_OFFICE_CHARTERS.json"
def registry(tmp_path):
 r=OfficeRegistry(tmp_path/"offices.json");result=load_charters(r,CHARTERS);return r,result
def test_dependency_ready_offices_are_registered_and_ai_office_is_honestly_deferred(tmp_path):
 r,result=registry(tmp_path);assert len(result["registered"])==10 and result["deferred"][0]["office_id"]=="OFFICE-000005" and "OFFICE-000005" not in r.data["offices"]
def test_security_recovery_evidence_routes_to_exactly_one_accountable_office(tmp_path):
 r,_=registry(tmp_path);row=r.route(WorkItem("WI-SEC-001","security","Review recovery drill","SECURITY-RECOVERY-001",{"verified":True}));assert row["office_id"]=="OFFICE-000011"
def test_decision_rights_and_evidence_are_enforced(tmp_path):
 r,_=registry(tmp_path);r.route(WorkItem("WI-AUTO-001","automation","Approve capability automation","CAPABILITY-FACTORY-001"))
 with pytest.raises(ValueError,match="unauthorized"):r.decide("WI-AUTO-001","APPROVE",{"blueprint":{},"validation":{}},"OTHER")
 with pytest.raises(ValueError,match="missing_decision_evidence"):r.decide("WI-AUTO-001","APPROVE",{"blueprint":{}},"AUTOMATION_DIRECTOR")
 assert r.decide("WI-AUTO-001","APPROVE",{"blueprint":{},"validation":{"passed":True}},"AUTOMATION_DIRECTOR")["status"]=="DECIDED"
def test_ambiguous_or_unknown_accountability_is_rejected(tmp_path):
 r,_=registry(tmp_path)
 with pytest.raises(ValueError,match="ambiguous_or_missing"):r.route(WorkItem("WI-X","unknown","No owner","test"))
