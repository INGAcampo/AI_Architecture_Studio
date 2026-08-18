import hashlib
import json

from aias_project_production.certification import certify_drawings_production_core


def test_drawings_certification_binds_bar_marks_sheets_qa_and_issuance(tmp_path):
    result = certify_drawings_production_core(tmp_path)

    assert result["verdict"] == "DRAWINGS_PRODUCTION_CORE_READY"
    assert all(result["checks"].values())
    assert result["estimated_time_reduction_percent"] >= 45
    assert result["classification"] == "PRELIMINARY_NOT_FOR_CONSTRUCTION"
    assert {item["project_id"] for item in result["projects"]} == {
        "DRAWINGS-CORE-CERT-A",
        "DRAWINGS-CORE-CERT-B",
    }
    for project in result["projects"]:
        path = tmp_path / project["evidence_file"]
        payload = json.loads(path.read_text(encoding="utf-8"))
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        assert digest == project["evidence_sha256"]
        assert payload["drawing_model"]["schema"] == "aias.drawing_model.v2"
        assert payload["drawing_model"]["annotations"]
        assert payload["drawing_model"]["design_trace"] == payload["qa_drawing_trace"]
        assert payload["qa_drawing_trace"] == payload["issuance_drawing_trace"]
        assert payload["NOT_FOR_CONSTRUCTION"] is True
