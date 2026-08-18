import hashlib
import json

from aias_project_production.certification import certify_design_production_core


def test_design_certification_exercises_nominal_and_stress_fail_closed(tmp_path):
    result = certify_design_production_core(tmp_path)

    assert result["verdict"] == "DESIGN_PRODUCTION_CORE_READY"
    assert all(result["checks"].values())
    assert result["scenario_faults_detected"] == ["DESIGN-CORE-CERT-B"]
    assert {item["scenario_id"] for item in result["projects"]} == {
        "NOMINAL_CASE_001", "STRESS_CASE_001"
    }

    normal = next(item for item in result["projects"] if not item["scenario_fault"])
    stress = next(item for item in result["projects"] if item["scenario_fault"])
    assert normal["bar_set_count"] > 0
    assert stress["bar_set_count"] == 0
    assert stress["status"] == "SCENARIO_FAILURE_DETECTED"

    for project in result["projects"]:
        path = tmp_path / project["evidence_file"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        assert digest == project["evidence_sha256"]

    normal_payload = json.loads((tmp_path / normal["evidence_file"]).read_text(encoding="utf-8"))
    assert normal_payload["quantity_trace"] == normal_payload["qa_reinforcement_trace"]
    assert normal_payload["reinforcement"] is not None

    stress_payload = json.loads((tmp_path / stress["evidence_file"]).read_text(encoding="utf-8"))
    fault = stress_payload["scenario_fault_evidence"]
    assert stress_payload["reinforcement"] is None
    assert stress_payload["quantity_trace"] is None
    assert stress_payload["qa_reinforcement_trace"] is None
    assert fault["failure_classification"] == "SCENARIO_DESIGN_FAILURE"
    assert fault["reinforcement_specification"] is None
    assert fault["bar_sets"] == []
    assert fault["schedules"] == []
