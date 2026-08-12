import json
from pathlib import Path
import pytest
from aias_aeks.models import KnowledgeUnit
from aias_executable_knowledge import KnowledgeAdmission,DeclarativeKnowledgeExecutor
ROOT=Path(__file__).resolve().parents[1];EKU=ROOT/"engineering/aias/aeks/EKU-000002-bearing-pressure.json"
def unit():return KnowledgeUnit(**json.loads(EKU.read_text(encoding="utf-8")))
def test_approved_unit_has_license_provenance_and_safe_execution():assert KnowledgeAdmission().validate(unit())==[]
def test_execution_is_reproducible_and_traceable():
 result=DeclarativeKnowledgeExecutor().execute(unit(),{"vertical_load_kn":800.0,"area_m2":5.0},"CALC-BEARING-001");assert result["output"]=={"name":"bearing_pressure_kpa","value":160.0,"unit":"kPa"} and len(result["evidence_sha256"])==64 and result["human_review_required"]
def test_input_rule_and_contract_are_enforced():
 engine=DeclarativeKnowledgeExecutor()
 with pytest.raises(ValueError,match="validation_rule_failed"):engine.execute(unit(),{"vertical_load_kn":800.0,"area_m2":0.0},"CALC-BEARING-001")
 with pytest.raises(ValueError,match="input_contract_mismatch"):engine.execute(unit(),{"area_m2":5.0},"CALC-BEARING-001")
def test_calls_and_attributes_cannot_execute():
 u=unit();u.calculations[0]["expression"]="__import__('os').system('echo unsafe')"
 with pytest.raises(ValueError,match="unsafe_expression"):DeclarativeKnowledgeExecutor().execute(u,{"vertical_load_kn":800.0,"area_m2":5.0},"CALC-BEARING-001")
