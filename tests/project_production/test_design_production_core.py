import hashlib
import json

from aias_project_production.certification import certify_design_production_core


def test_design_certification_binds_analysis_standards_quantities_and_qa(tmp_path):
    result = certify_design_production_core(tmp_path)

    assert result["verdict"] == "DESIGN_PRODUCTION_CORE_READY"
    assert all(result["checks"].values())
    assert result["estimated_time_reduction_percent"] >= 45
    assert result["classification"] == "PRELIMINARY_NOT_FOR_CONSTRUCTION"
    assert {item["project_id"] for item in result["projects"]} == {
        "DESIGN-CORE-CERT-A",
        "DESIGN-CORE-CERT-B",
    }
    for project in result["projects"]:
        path = tmp_path / project["evidence_file"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        assert digest == project["evidence_sha256"]
        assert payload["quantity_trace"] == payload["qa_reinforcement_trace"]
        assert payload["NOT_FOR_CONSTRUCTION"] is True
