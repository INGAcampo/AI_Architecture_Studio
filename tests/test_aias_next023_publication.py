import json
from pathlib import Path

from aias_next023_publication import MetricsPublicationGate


def test_reference_metric_is_labeled_not_audited(tmp_path: Path):
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps({"acceleration": {"audited": False, "classification": "REFERENCE_ENGINEERING_ESTIMATE"}}), encoding="utf-8")
    decision = MetricsPublicationGate(snapshot).evaluate()
    assert decision.allowed is True
    assert decision.label == "REFERENCE_ESTIMATE_NOT_AUDITED"
