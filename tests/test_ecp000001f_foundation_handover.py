import json
import pytest
from aias_foundation_delivery.orchestrator import FoundationDeliveryOrchestrator
from aias_foundation_handover.acceptance import evaluate
from aias_foundation_handover.custody import verify_transmittal
from aias_foundation_handover.engine import FoundationHandoverEngine
from aias_foundation_handover.kpi import calculate
from aias_foundation_handover.maturity import assess
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator

@pytest.fixture()
def transmittal(tmp_path):
    workspace=tmp_path/"delivery"; FoundationDeliveryOrchestrator().execute(workspace); return workspace/"transmittal"

def test_consumes_and_verifies_ecpe(transmittal): assert verify_transmittal(transmittal)["valid"]
def test_tampering_is_detected(transmittal):
    path=transmittal/"drawings"/"foundation_plan.svg"; path.write_text("tampered",encoding="utf-8"); assert not verify_transmittal(transmittal)["valid"]
def test_reference_delivery_passes_lifecycle_not_construction(transmittal):
    result=evaluate(verify_transmittal(transmittal)); assert result["lifecycle_accepted"] and not result["construction_accepted"]
def test_engine_creates_linked_custody_event(transmittal):
    result=FoundationHandoverEngine().build(transmittal); assert result["custody"][0]["previous_hash"]=="GENESIS" and len(result["custody"][0]["event_hash"])==64
def test_kpi_enforces_45_percent_target(): assert calculate(4,1.8,1.2,4,6).meets_45_percent_target
def test_invalid_kpi_is_rejected():
    with pytest.raises(ValueError): calculate(1,2,0,0,1)
def test_maturity_level_five_requires_full_loop():
    evidence={"repeatable_delivery":True,"traceability":True,"automated_quality_gates":True,"measured_acceleration":True,"continuous_improvement_loop":True}; assert assess(evidence)["level"]==5
def test_missing_improvement_loop_stops_at_four():
    evidence={"repeatable_delivery":True,"traceability":True,"automated_quality_gates":True,"measured_acceleration":True,"continuous_improvement_loop":False}; assert assess(evidence)["level"]==4
def test_orchestrator_writes_dossier_and_release(tmp_path):
    result=FoundationHandoverOrchestrator().execute(tmp_path/"handover"); dossier=tmp_path/"handover"/"lifecycle_dossier"/"FOUNDATION_HANDOVER_DOSSIER.json"; assert result["validated"] and dossier.is_file() and json.loads(dossier.read_text())["maturity"]["level"]==5
def test_estimate_is_not_misrepresented_as_audit(transmittal): assert FoundationHandoverEngine().build(transmittal)["kpi"]["classification"]=="REFERENCE_ENGINEERING_ESTIMATE"
