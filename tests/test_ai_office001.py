from pathlib import Path
import pytest
from aias_enterprise_offices import OfficeRegistry
from aias_enterprise_offices.ai_office import activate_ai_office,route_intelligence_case
ROOT=Path(__file__).resolve().parents[1];CHARTER=ROOT/"engineering/aias/offices/AI_OFFICE_CHARTER.json"
def test_ai_office_cannot_activate_before_intelligence_core(tmp_path):
 with pytest.raises(ValueError,match="SYS-000012"):activate_ai_office(OfficeRegistry(tmp_path/"r.json"),CHARTER,set())
def test_ai_office_activates_and_owns_intelligence_governance(tmp_path):
 registry=OfficeRegistry(tmp_path/"r.json");result=activate_ai_office(registry,CHARTER,{"SYS-000012"});case=route_intelligence_case(registry,"AI-CASE-001",{"recommendation":"INT-FOUND-001","confidence":.95});assert result["activated"] and case["office_id"]=="OFFICE-000005"
def test_ai_decision_requires_all_governance_evidence(tmp_path):
 registry=OfficeRegistry(tmp_path/"r.json");activate_ai_office(registry,CHARTER,{"SYS-000012"});route_intelligence_case(registry,"AI-CASE-001",{})
 with pytest.raises(ValueError,match="missing_decision_evidence"):registry.decide("AI-CASE-001","ACCEPT",{"model_card":{}},"AI_GOVERNANCE_DIRECTOR")
 row=registry.decide("AI-CASE-001","ACCEPT",{"model_card":{},"evaluation":{},"risk_assessment":{},"human_oversight_plan":{}},"AI_GOVERNANCE_DIRECTOR");assert row["status"]=="DECIDED"
