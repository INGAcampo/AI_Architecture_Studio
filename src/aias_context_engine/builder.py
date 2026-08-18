"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ContextManifest
from .scanner import RepositoryScanner


PERMANENT_RULES = [
    "The specification is the primary source of truth.",
    "Every macro-delivery must include code, tests, documentation, installer and release evidence.",
    "Do not declare completion without executable validation.",
    "Preserve modular architecture and reversible integration.",
    "Every new engine must have an immediate real consumer.",
    "Regulated engineering output requires traceability and professional review.",
    "AI modifications must pass validation, transaction history, undo and audit controls.",
    "Prefer reusable engineering capabilities over isolated feature accumulation.",
    "Preserve existing user work and never overwrite unrelated changes.",
]


class ContextBuilder:
    """Execute the public ContextBuilder operation for the AIAS continuity and context system using explicit caller inputs."""
    SCHEMA_VERSION = "1.0.0"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, project_root: Path):
        self.root = project_root.resolve()
        self.scanner = RepositoryScanner(self.root)

    def build(self) -> dict[str, Any]:
        """Build the build required by the AIAS continuity and context system from explicit inputs."""
        components = self.scanner.components()
        component_ids = {c.component_id for c in components}
        plan_path = self.root / "engineering" / "aias" / "master" / "AIAS_MASTER_DEVELOPMENT_PLAN.json"
        try:
            development_plan = json.loads(plan_path.read_text(encoding="utf-8")) if plan_path.is_file() else {}
        except (OSError, json.JSONDecodeError):
            development_plan = {}
        current_program = development_plan.get("current", "ROADMAP-AUDIT-001 Integral Completion Audit - VALIDATED")
        next_program = development_plan.get("next", "EXTERNAL-GATES-001 Licensed Standards, Vendor Runtimes, Independent Review and Longitudinal Evidence")
        completed = [
            item for item in (
                "AIAS_AMP010A_ENTERPRISE_CALCULATION_FRAMEWORK_INSTALLER",
                "AIAS_AMP010B_GEOMETRY_KERNEL_INSTALLER",
                "AIAS_AMP010C_ENGINEERING_OBJECT_KERNEL_INSTALLER",
                "AIAS_ECP000001A_FOUNDATION_OBJECT_LIBRARY_INSTALLER",
                "AIAS_ECP000001B_FOUNDATION_CALCULATION_ENGINE_INSTALLER",
                "AIAS_ECP000001C_FOUNDATION_CODE_CHECK_FRAMEWORK_INSTALLER",
                "AIAS_ECP000001D_FOUNDATION_DETAILING_DOCUMENTATION_INSTALLER",
                "AIAS_ECP000001E_FOUNDATION_COORDINATION_DELIVERY_INSTALLER",
                "AIAS_ECP000001F_FOUNDATION_DIGITAL_HANDOVER_INSTALLER",
                "AIAS_ECP000001G_TECHNOLOGY_OBSERVATORY_INSTALLER",
                "AIAS_GOV000049_HISTORICAL_DECISION_SDD_ASSURANCE_INSTALLER",
                "AIAS_DOC_ALIGN_001_ACTIVE_PACKAGES_INSTALLER",
                "AIAS_AIPD000001_PRODUCTIVITY_DASHBOARD_INSTALLER",
                "AIAS_AMIR000001_MASTER_INVENTORY_ROADMAP_INSTALLER",
                "AIAS_LIGHTHOUSE000001_REFERENCE_BUILDING_INSTALLER",
                "AIAS_FOUNDATION_ALIGN001_CHARTER_HANDBOOK_INSTALLER",
                "AIAS_FOUNDATION_ALIGN002_ENGINEERING_SYSTEM_AES_INSTALLER",
                "AIAS_ASSET_REGISTRY001_UNIVERSAL_REGISTRY_INSTALLER",
                "AIAS_DOC_ALIGN_002_COMPLETE_PUBLIC_API_INSTALLER",
                "AIAS_ATO000002_CONTINUOUS_OBSERVATORY_INSTALLER",
                "AIAS_UNIVERSITY_FOUNDATION001_INSTALLER",
                "AIAS_CNS000001_CENTRAL_NERVOUS_SYSTEM_INSTALLER",
                "AIAS_PMO000001_PORTFOLIO_MANAGEMENT_INSTALLER",
                "AIAS_AEKS_ALIGN001_EXECUTABLE_KNOWLEDGE_INSTALLER",
                "AIAS_EKG000001_ENTERPRISE_KNOWLEDGE_GRAPH_INSTALLER",
                "AIAS_DEV_PLATFORM001_UNIFIED_DEVELOPMENT_PLATFORM_INSTALLER",
                "AIAS_CAPABILITY_FACTORY001_GOVERNED_FACTORY_INSTALLER",
                "AIAS_SECURITY_RECOVERY001_VERIFIABLE_RECOVERY_INSTALLER",
                "AIAS_OFFICES_FOUNDATION001_ENTERPRISE_OFFICES_INSTALLER",
                "AIAS_ENGINEERING_WAVE12001_ASSURANCE_FOUNDATIONS_INSTALLER",
                "AIAS_DRAWING_FRAMEWORK001_ENTERPRISE_DRAWING_INSTALLER",
                "AIAS_CAD_BIM_INTEGRATION001_CANONICAL_BRIDGE_INSTALLER",
                "AIAS_TECHNICAL_FILE001_ENTERPRISE_DOSSIER_INSTALLER",
                "AIAS_VIRTUAL_ORG001_ENGINEERING_WORKFORCE_INSTALLER",
                "AIAS_INTELLIGENCE_CORE001_EVIDENCE_INTELLIGENCE_INSTALLER",
                "AIAS_AI_OFFICE001_GOVERNANCE_ACTIVATION_INSTALLER",
                "AIAS_AEOS000001_ENGINEERING_OPERATING_SYSTEM_INSTALLER",
                "AIAS_AUTONOMOUS_CLOUD001_CLOUD_NEUTRAL_CONTROL_PLANE_INSTALLER",
                "AIAS_LEVEL5_ASSURANCE001_MATURITY_ASSURANCE_INSTALLER",
                "AIAS_END_TO_END001_PROJECT_PRODUCTION_INSTALLER",
                "AIAS_LEVEL5_EVIDENCE_CAMPAIGN001_LONGITUDINAL_LEDGER_INSTALLER",
                "AIAS_CERTIFICATION_MASTER_PLAN001_EXTERNAL_ASSURANCE_INSTALLER",
                "AIAS_GOV_CONTINUITY001_VERIFIABLE_HANDOFF_INSTALLER",
                "AIAS_CERTIFICATION_IMS_FOUNDATION001_INTEGRATED_SYSTEM_INSTALLER",
                "AIAS_CERTIFICATION_NORMATIVE_ACCESS001_PROCUREMENT_READINESS_INSTALLER",
                "AIAS_STRUCTURAL_CODES_PROGRAM001_LIVING_KNOWLEDGE_INSTALLER",
                "AIAS_DESIGN_SYSTEM001_EXPERIENCE_FOUNDATION_INSTALLER",
                "AIAS_UX_AUDIT001_WORKSPACE2_BASELINE_INSTALLER",
                "AIAS_WORKSPACE2_FOUNDATION_INSTALLER",
                "AIAS_WORKSPACE2_W2_02_ORCHESTRATION_INSTALLER",
                "AIAS_WORKSPACE2_W2_03_BIM_INSPECTOR_INSTALLER",
                "AIAS_WORKSPACE2_W2_04_COMMAND_STATUS_INSTALLER",
                "AIAS_WORKSPACE2_W2_05_LIGHTHOUSE_JOURNEY_INSTALLER",
                "AIAS_WORKSPACE2_W2_06_COORDINATION_LEARNING_INSTALLER",
                "AIAS_WORKSPACE2_W2_07_VALIDATION_CAMPAIGN_INSTALLER",
                "AIAS_EXP_INSTALLER_ISO001_DISTRIBUTION_FOUNDATION_INSTALLER",
            ) if item in component_ids
        ]
        manifest = ContextManifest(
            schema_version=self.SCHEMA_VERSION,
            engine_version=self.ENGINE_VERSION,
            generated_at=datetime.now(timezone.utc).isoformat(),
            project_root=str(self.root),
            identity={
                "project_id": "AIAS",
                "name": "AI Architecture Studio",
                "kind": "Unified CAD/BIM/Engineering and AI platform",
                "mission": "Produce reusable, traceable and professionally verifiable engineering capabilities.",
            },
            constitution={
                "status": "ACTIVE",
                "development_model": "SPECIFICATION_DRIVEN_CAPABILITY_BASED",
                "minimum_sustainable_time_reduction_percent": 45,
                "hierarchy": ["Constitution", "SDD Methodology", "Architecture Handbook", "Program Specifications", "Module Specifications", "Generated Artifacts"],
            },
            current_state={
                "status": "ACTIVE_DEVELOPMENT",
                "active_program": current_program,
                "completed_foundation_chain": completed,
                "repository": self.scanner.test_inventory(),
                "source_package_count": len(self.scanner.source_packages()),
                "constitutional_compliance": self.scanner.constitutional_compliance(),
            },
            roadmap={
                "current": current_program,
                "next": next_program,
                "sequence": ["ACE-000001", "ECP-000001D", "ECP-000001E", "ECP-000001F", "ECP-000001G/ATO", "GOV-000049", "DOC-ALIGN-001", "DOC-ALIGN-002", "ATO-000002", "AIAS University Foundation"],
            },
            components=components,
            installed_packages=self.scanner.source_packages(),
            programs_in_progress=[{"id": "ACE-000001", "status": "ACTIVE_INFRASTRUCTURE", "consumer": "Every future AIAS macro-delivery"}, {"id": "AIAS-WORKSPACE-2.0", "status": "AUTOMATED_VALIDATION_PASSED_REPRESENTATIVE_SESSIONS_ACTIVE", "consumer": "AIAS professional desktop"}, {"id": "LEVEL5-EVIDENCE-CAMPAIGN-001", "status": "ACTIVE_EVIDENCE_COLLECTION"}, {"id": "CERTIFICATION-NORMATIVE-ACCESS-001", "status": "VALIDATED_NO_COMMERCIAL_ACTION"}],
            permanent_rules=PERMANENT_RULES + ["AEC-000049: materialize technically correct, verifiable, maintainable and legally compatible value at the earliest maturity level.", "AEC-000050: communicate material opportunities, risks and acceleration recommendations immediately with evidence, tradeoffs and a concrete action; suppress non-actionable noise.", "AEC-000051: before migrating, replacing or promoting a fork as the primary AIAS conversation, generate and validate a repository-derived checksum-protected continuity package.", "AEC-000052: apply maximum stewardship, initiative and exceptional coherent experience across every AIAS surface without unsupported claims."],
            aias_university={"status": "OPERATIONAL_FOUNDATION", "catalog": "engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json", "capabilities": ["tutorials", "manuals", "guides", "courses", "exams", "verifiable_internal_credentials"], "professional_license": False},
            decisions=[
                {"id": "CONST-0001", "decision": "Architectural decisions must reduce development time sustainably while preserving quality and traceability."},
                {"id": "OE-000031", "decision": "Tangible implementation has priority over conceptual expansion."},
                {"id": "ACE-DEC-0001", "decision": "ACE precedes the next engineering engine and becomes the continuity source of truth."},
            ],
            knowledge_graph={"nodes": ["AIAS", "ACE", "AEPS", "ADF", "AEKS", "AMP-010A", "AMP-010B", "AMP-010C", "ECP-000001"], "edges": [["ACE", "preserves", "AIAS"], ["AEPS", "produces", "capabilities"], ["ECP-000001C", "feeds", "ECP-000001D"], ["ECP-000001D", "feeds", "ECP-000001E"], ["ECP-000001E", "feeds", "ECP-000001F"]]},
            engineering_object_index={"kernel": "AMP-010C", "status": "INSTALLED" if "AIAS_AMP010C_ENGINEERING_OBJECT_KERNEL_INSTALLER" in component_ids else "UNKNOWN"},
            capabilities=["context_capture", "repository_inventory", "versioned_snapshots", "integrity_validation", "continuity_packaging", "roadmap_reconciliation"],
            sprint_history=[{"id": item, "status": "COMPLETED"} for item in completed],
            changelog=[{"event": "ACE_CONTEXT_GENERATED", "timestamp": datetime.now(timezone.utc).isoformat()}],
            artifacts=self.scanner.artifacts(),
        )
        data = manifest.to_dict()
        canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        data["integrity"] = {"algorithm": "SHA-256", "canonical_payload_sha256": hashlib.sha256(canonical).hexdigest()}
        return data
