import json
from pathlib import Path

from scripts.generate_constitutional_compliance import DEFINITIONS, generate


def test_definitions_cover_ace_and_foundation_delivery_chain():
    expected = {"ACE-000001", "ECP-000001D", "ECP-000001E", "ECP-000001F", "ECP-000001G", "GOV-000049", "AIPD-000001", "AMIR-000001", "LIGHTHOUSE-000001", "FOUNDATION-ALIGN-001", "FOUNDATION-ALIGN-002", "ASSET-REGISTRY-001", "DOC-ALIGN-002", "ATO-000002", "UNIVERSITY-FOUNDATION-001", "CNS-000001", "PMO-000001", "AEKS-ALIGN-001", "EKG-000001", "DEV-PLATFORM-001", "CAPABILITY-FACTORY-001", "SECURITY-RECOVERY-001", "OFFICES-FOUNDATION-001", "ENGINEERING-WAVE12-001", "DRAWING-FRAMEWORK-001", "CAD-BIM-INTEGRATION-001", "TECHNICAL-FILE-001", "VIRTUAL-ORG-001", "INTELLIGENCE-CORE-001", "AI-OFFICE-001", "AEOS-000001", "AUTONOMOUS-CLOUD-001", "LEVEL5-ASSURANCE-001", "END-TO-END-001", "LEVEL5-EVIDENCE-CAMPAIGN-001", "CERTIFICATION-MASTER-PLAN-001", "GOV-CONTINUITY-001", "CERTIFICATION-IMS-FOUNDATION-001", "CERTIFICATION-NORMATIVE-ACCESS-001"}
    assert set(DEFINITIONS) == expected


def test_all_constitutional_gates_pass():
    for component in DEFINITIONS:
        report = generate(component)
        assert report["all_passed"]
        assert all(gate["passed"] for gate in report["gates"])
        assert report["kpi"]["meets_45_percent_target"]


def test_compliance_artifacts_are_complete():
    root = Path(__file__).resolve().parents[1]
    for component, definition in DEFINITIONS.items():
        generate(component)
        folder = root / "engineering" / definition["folder"] / "compliance"
        assert (folder / "ASDD.json").exists()
        assert (folder / "TRACEABILITY.json").exists()
        assert (folder / "QUALITY_GATES.json").exists()
        report = json.loads((folder / "QUALITY_GATES.json").read_text(encoding="utf-8"))
        assert report["validator_issues"] == []
