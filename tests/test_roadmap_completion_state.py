import json
from pathlib import Path

from aias_governance_assurance.orchestrator import GovernanceAssuranceOrchestrator
from aias_master_inventory.lighthouse import contract

ROOT = Path(__file__).resolve().parents[1]


def test_current_repository_has_no_documentation_or_sdd_alignment_backlog(tmp_path):
    result = GovernanceAssuranceOrchestrator().execute(ROOT, tmp_path)
    plan = json.loads((tmp_path / "AIAS_MASTER_DEVELOPMENT_PLAN.json").read_text(encoding="utf-8"))
    assert result["alignment_items"] == 0
    assert plan["backlog"] == []
    assert plan["current"].startswith("CERTIFICATION-NORMATIVE-ACCESS-001")
    assert plan["next"].startswith("CERTIFICATION-EXTERNAL-SELECTION-001")


def test_lighthouse_contract_matches_operating_reference_evidence():
    row = contract()
    assert row["status"] == "OPERATING_REFERENCE_FOR_REVIEW"
    assert all((ROOT / path).exists() for path in row["evidence"])
