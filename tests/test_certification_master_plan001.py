import json
from pathlib import Path

from aias_certification_program import CertificationReadinessAssessor, official_frameworks

ROOT = Path(__file__).resolve().parents[1]


def test_official_portfolio_has_one_primary_maturity_objective_and_ai_extension():
    rows = official_frameworks()
    assert len(rows) == 6
    assert sum(row["role"] == "PRIMARY_ORGANIZATIONAL_MATURITY_OBJECTIVE" for row in rows) == 1
    assert any(row["id"] == "CMMI-AIM" and row["role"] == "MANDATORY_AI_MATURITY_EXTENSION" for row in rows)


def test_iso_ai_management_is_mandatory_not_omitted():
    assert any(row["id"] == "ISO-IEC-42001" and row["role"] == "AI_MANAGEMENT_CERTIFICATION" for row in official_frameworks())


def test_plan_separates_internal_gate_from_official_cmmi_requirements():
    plan = json.loads((ROOT / "engineering/aias/certification/AIAS_CERTIFICATION_MASTER_PLAN.json").read_text(encoding="utf-8"))
    assert plan["official_maturity_objective"] == "CMMI Development V3.0 Maturity Level 5"
    assert plan["internal_readiness_gate"]["classification"] == "AIAS_INTERNAL_PRUDENTIAL_GATE_NOT_AN_OFFICIAL_CMMI_REQUIREMENT"
    assert not plan["decision_boundaries"]["aias_self_certification_permitted"]


def test_readiness_assessment_never_claims_external_certification():
    result = CertificationReadinessAssessor().assess(ROOT)
    assert result["classification"] == "INTERNAL_READINESS_NOT_CERTIFICATION"
    assert not result["certification_claim_permitted"]
    assert all(not row["externally_certified_or_rated"] and row["external_assessment_required"] for row in result["frameworks"])
    assert len(result["evidence_sha256"]) == 64
