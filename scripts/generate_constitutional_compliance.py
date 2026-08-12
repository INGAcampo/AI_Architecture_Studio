from __future__ import annotations

# AIAS_SRC_PATH_BOOTSTRAP
from pathlib import Path as _AIASPath
import sys as _aias_sys
_AIAS_ROOT = _AIASPath(__file__).resolve().parents[1]
_AIAS_SRC = str(_AIAS_ROOT / 'src')
if _AIAS_SRC not in _aias_sys.path:
    _aias_sys.path.insert(0, _AIAS_SRC)

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from aias_aeps_governance_sdd.kpi import ProductivitySnapshot
from aias_aeps_governance_sdd.models import Requirement, RequirementStatus, RequirementType, Specification
from aias_aeps_governance_sdd.quality import QualityGateEngine
from aias_aeps_governance_sdd.traceability import TraceabilityMatrix
from aias_aeps_governance_sdd.validators import SpecificationValidator


ROOT = Path(__file__).resolve().parents[1]


DEFINITIONS = {
    "ACE-000001": {
        "folder": "ace000001",
        "spec_id": "SPEC-100001",
        "title": "AIAS Context Engine",
        "purpose": "Provide a repository-derived, versioned and integrity-protected continuity authority for AIAS.",
        "scope": "Context inventory, roadmap reconciliation, snapshots, integrity validation and continuity artifacts.",
        "arch": "ARCH-ACE-000001",
        "adr": "ADR-ACE-000001",
        "requirements": [
            ("REQ-100001", "Repository context", "ACE shall derive the current project state from the active repository.", "Prevent stale chat summaries from becoming project authority.", "src/aias_context_engine/builder.py", "tests/test_ace_context_engine.py"),
            ("REQ-100002", "Versioned snapshots", "ACE shall create a versioned context snapshot after each build.", "Preserve historical continuity.", "src/aias_context_engine/storage.py", "tests/test_ace_context_engine.py"),
            ("REQ-100003", "Integrity", "ACE shall protect the canonical context with SHA-256 integrity validation.", "Detect unauthorized or accidental changes.", "src/aias_context_engine/validator.py", "tests/test_ace_context_engine.py"),
            ("REQ-100004", "Roadmap reconciliation", "ACE shall reconcile completed components and the next formal program.", "Continue from verified repository state.", "src/aias_context_engine/scanner.py", "tests/test_ace_context_engine.py"),
            ("REQ-100005", "Continuity artifacts", "ACE shall generate machine-readable and human-readable continuity artifacts.", "Allow reliable transfer between conversations and models.", "src/aias_context_engine/storage.py", "tests/test_ace_context_engine.py"),
        ],
        "baseline_hours": 2.0,
        "actual_hours": 0.25,
        "automated_hours": 0.20,
        "reused_assets": 4,
        "total_assets": 5,
    },
    "ECP-000001D": {
        "folder": "ecp000001d",
        "spec_id": "SPEC-200001",
        "title": "Foundation Detailing and Documentation",
        "purpose": "Transform validated foundation objects, calculations and checks into traceable technical documentation.",
        "scope": "SVG drawings, reinforcement schedule, quantities, technical reports, QA evidence and release packaging.",
        "arch": "ARCH-ECP-000001D",
        "adr": "ADR-ECP-000001D",
        "requirements": [
            ("REQ-200001", "Chain consumption", "ECP-000001D shall consume outputs from ECP-000001A, ECP-000001B and ECP-000001C.", "Maintain a real vertical engineering workflow.", "src/aias_foundation_documentation/engine.py", "tests/test_ecp000001d_foundation_documentation.py"),
            ("REQ-200002", "Foundation drawings", "The system shall generate a foundation plan and section as vector drawings.", "Produce immediate technical artifacts.", "src/aias_foundation_documentation/drawings.py", "tests/test_ecp000001d_foundation_documentation.py"),
            ("REQ-200003", "Reinforcement schedule", "The system shall generate a traceable reinforcement bar schedule.", "Support detailing and quantity workflows.", "src/aias_foundation_documentation/detailing.py", "tests/test_ecp000001d_foundation_documentation.py"),
            ("REQ-200004", "Quantities", "The system shall calculate concrete, formwork, excavation and reinforcement quantities.", "Enable downstream delivery and estimating consumers.", "src/aias_foundation_documentation/quantities.py", "tests/test_ecp000001d_foundation_documentation.py"),
            ("REQ-200005", "Technical package", "The system shall generate JSON, CSV, Markdown and release artifacts with checksum evidence.", "Provide a reproducible professional package.", "src/aias_foundation_documentation/orchestrator.py", "tests/test_ecp000001d_foundation_documentation.py"),
            ("REQ-200006", "Regulatory controls", "The system shall preserve legal status and require professional review for construction use.", "Prevent reference equations from being misrepresented as approved design documents.", "src/aias_foundation_documentation/engine.py", "tests/test_ecp000001d_foundation_documentation.py"),
        ],
        "baseline_hours": 8.0,
        "actual_hours": 0.5,
        "automated_hours": 0.45,
        "reused_assets": 3,
        "total_assets": 4,
    },
    "ECP-000001E": {
        "folder": "ecp000001e",
        "spec_id": "SPEC-200002",
        "title": "Foundation Coordination and Delivery Framework",
        "purpose": "Coordinate, verify, revise and transmit the technical foundation package produced by ECP-000001D.",
        "scope": "Deliverable completeness, revision manifests, issue register, approval controls, checksums and transmittal packaging.",
        "arch": "ARCH-ECP-000001E",
        "adr": "ADR-ECP-000001E",
        "status": "VALIDATED",
        "requirements": [
            ("REQ-200101", "ECP-D consumption", "ECP-000001E shall consume the complete technical package produced by ECP-000001D.", "Maintain an immediate real consumer for detailing outputs.", "src/aias_foundation_delivery/engine.py", "tests/test_ecp000001e_foundation_delivery.py"),
            ("REQ-200102", "Completeness validation", "The system shall verify required drawings, schedules, reports and QA evidence before delivery.", "Prevent incomplete technical transmittals.", "src/aias_foundation_delivery/validation.py", "tests/test_ecp000001e_foundation_delivery.py"),
            ("REQ-200103", "Revision control", "The system shall create immutable revision manifests with file checksums.", "Provide reproducible delivery history.", "src/aias_foundation_delivery/revisions.py", "tests/test_ecp000001e_foundation_delivery.py"),
            ("REQ-200104", "Issue register", "The system shall maintain traceable coordination issues and resolution status.", "Support multidisciplinary review.", "src/aias_foundation_delivery/issues.py", "tests/test_ecp000001e_foundation_delivery.py"),
            ("REQ-200105", "Transmittal package", "The system shall generate a versioned transmittal archive and machine-readable manifest.", "Create a tangible downstream delivery asset.", "src/aias_foundation_delivery/orchestrator.py", "tests/test_ecp000001e_foundation_delivery.py"),
            ("REQ-200106", "Approval control", "The system shall prevent construction-approved status without verified official code status and professional approval evidence.", "Preserve regulatory and professional responsibility.", "src/aias_foundation_delivery/validation.py", "tests/test_ecp000001e_foundation_delivery.py"),
        ],
        "baseline_hours": 3.0,
        "actual_hours": 0.3,
        "automated_hours": 0.25,
        "reused_assets": 4,
        "total_assets": 5,
        "kpi_classification": "REFERENCE_ENGINEERING_ESTIMATE",
        "kpi_warning": "Post-validation reference productivity estimate; not an independently audited labor study.",
    },
    "ECP-000001F": {
        "folder": "ecp000001f",
        "spec_id": "SPEC-200003",
        "title": "Foundation Digital Handover and Lifecycle Assurance Framework",
        "purpose": "Convert the controlled ECP-000001E transmittal into an auditable digital handover with custody, acceptance, KPI and continuous-improvement evidence.",
        "scope": "Transmittal ingestion, checksum verification, custody ledger, acceptance gates, maturity assessment, KPI evidence, findings and lifecycle dossier packaging.",
        "arch": "ARCH-ECP-000001F",
        "adr": "ADR-ECP-000001F",
        "status": "VALIDATED",
        "requirements": [
            ("REQ-200201", "ECP-E consumption", "ECP-000001F shall consume and identify a complete ECP-000001E transmittal.", "Preserve the real vertical consumer chain.", "src/aias_foundation_handover/engine.py", "tests/test_ecp000001f_foundation_handover.py"),
            ("REQ-200202", "Custody integrity", "The system shall independently verify every transmitted file and record an append-only custody event.", "Detect corruption and preserve delivery provenance.", "src/aias_foundation_handover/custody.py", "tests/test_ecp000001f_foundation_handover.py"),
            ("REQ-200203", "Acceptance controls", "The system shall evaluate completeness, integrity, issue and professional-approval acceptance gates.", "Prevent unsafe or incomplete lifecycle acceptance.", "src/aias_foundation_handover/acceptance.py", "tests/test_ecp000001f_foundation_handover.py"),
            ("REQ-200204", "Maturity evidence", "The system shall calculate a reproducible five-level capability assessment from explicit gate evidence.", "Provide measurable progress toward AIAS Level 5.", "src/aias_foundation_handover/maturity.py", "tests/test_ecp000001f_foundation_handover.py"),
            ("REQ-200205", "Sustainable acceleration", "The system shall record baseline, actual, automation and reuse evidence and distinguish estimates from audited measurements.", "Enforce the constitutional 45 percent target without unsupported claims.", "src/aias_foundation_handover/kpi.py", "tests/test_ecp000001f_foundation_handover.py"),
            ("REQ-200206", "Lifecycle dossier", "The system shall generate a versioned machine-readable dossier, findings register and checksum-protected release archive.", "Create a tangible reusable handover asset.", "src/aias_foundation_handover/orchestrator.py", "tests/test_ecp000001f_foundation_handover.py"),
        ],
        "baseline_hours": 4.0,
        "actual_hours": 1.8,
        "automated_hours": 1.2,
        "reused_assets": 4,
        "total_assets": 6,
        "kpi_classification": "REFERENCE_ENGINEERING_ESTIMATE",
        "kpi_warning": "Post-validation reference-case evidence; organization-wide Level 5 requires production measurements and independent audit.",
    },
    "ECP-000001G": {
        "folder": "ecp000001g",
        "spec_id": "SPEC-200004",
        "title": "AIAS Technology Observatory",
        "purpose": "Continuously identify and govern world knowledge capable of producing large, sustainable advances in AIAS and materialize safe value at the earliest maturity level.",
        "scope": "Authoritative-source registry, observation evidence, relevance and impact scoring, constitutional filtering, opportunity portfolio, immediate-value actions and intelligence release packaging.",
        "arch": "ARCH-ECP-000001G-ATO",
        "adr": "ADR-ECP-000001G-ATO",
        "status": "VALIDATED",
        "requirements": [
            ("REQ-200301", "Global evidence", "ATO shall register dated, attributable and integrity-protected observations from authoritative world sources.", "Keep technology intelligence verifiable.", "src/aias_technology_observatory/sources.py", "tests/test_ecp000001g_technology_observatory.py"),
            ("REQ-200302", "Constitutional filter", "ATO shall reject opportunities that lack verification, maintainability, compatibility or legal review status.", "Enforce AEC-000049 without compromising higher obligations.", "src/aias_technology_observatory/governance.py", "tests/test_ecp000001g_technology_observatory.py"),
            ("REQ-200303", "Giant-step scoring", "ATO shall score relevance, impact, reuse, acceleration, risk and evidence strength reproducibly.", "Prioritize high-leverage opportunities.", "src/aias_technology_observatory/scoring.py", "tests/test_ecp000001g_technology_observatory.py"),
            ("REQ-200304", "ECP-F consumption", "ATO shall consume ECP-000001F maturity, findings and KPI evidence when prioritizing opportunities.", "Create a real feedback consumer for lifecycle evidence.", "src/aias_technology_observatory/engine.py", "tests/test_ecp000001g_technology_observatory.py"),
            ("REQ-200305", "Immediate value", "ATO shall emit a concrete earliest-maturity action for every accepted opportunity.", "Execute AEC-000049 as an operational rule.", "src/aias_technology_observatory/materialization.py", "tests/test_ecp000001g_technology_observatory.py"),
            ("REQ-200306", "Intelligence release", "ATO shall generate a versioned portfolio, source ledger, decision log and checksum-protected release.", "Provide reusable and auditable technology intelligence.", "src/aias_technology_observatory/orchestrator.py", "tests/test_ecp000001g_technology_observatory.py"),
        ],
        "baseline_hours": 10.0, "actual_hours": 4.0, "automated_hours": 3.0, "reused_assets": 5, "total_assets": 7,
        "kpi_classification": "REFERENCE_ENGINEERING_ESTIMATE",
        "kpi_warning": "Post-validation reference evidence; recurring production observations require auditable elapsed-time telemetry.",
    },
    "GOV-000049": {
        "folder": "gov000049",
        "spec_id": "SPEC-900049",
        "title": "Historical Decision Materialization and SDD Assurance",
        "purpose": "Recover approved AIAS development decisions, distinguish binding rules from future programs, audit their repository evidence and materialize missing governance controls immediately.",
        "scope": "Decision registry, SDD enforcement, documentation coverage, asset state/version controls, Definition of Done, anti-bureaucracy, executive metrics and master development plan evidence.",
        "arch": "ARCH-GOV-000049",
        "adr": "ADR-GOV-000049",
        "status": "VALIDATED",
        "requirements": [
            ("REQ-900401", "Decision registry", "The system shall preserve every recovered binding decision with capture provenance, classification and evidence links.", "Prevent historical governance loss.", "src/aias_governance_assurance/decisions.py", "tests/test_gov000049_governance_assurance.py"),
            ("REQ-900402", "SDD assurance", "The system shall verify specification, architecture, ADR, implementation, tests and traceability before a capability is validated.", "Make specification-driven development executable.", "src/aias_governance_assurance/sdd.py", "tests/test_gov000049_governance_assurance.py"),
            ("REQ-900403", "Documentation audit", "The system shall measure package, module and public-symbol documentation coverage without claiming undocumented code is complete.", "Create an honest documentation baseline and backlog.", "src/aias_governance_assurance/documentation.py", "tests/test_gov000049_governance_assurance.py"),
            ("REQ-900404", "Asset lifecycle", "The system shall enforce stable identifiers, semantic versions and one official lifecycle state per engineering asset.", "Version knowledge as well as code.", "src/aias_governance_assurance/assets.py", "tests/test_gov000049_governance_assurance.py"),
            ("REQ-900405", "Executable Definition of Done", "The system shall evaluate code, tests, integration, documentation, CLI, receipt, manifest, example, installer, release and validation evidence.", "Prevent premature completion claims.", "src/aias_governance_assurance/dod.py", "tests/test_gov000049_governance_assurance.py"),
            ("REQ-900406", "Master evidence", "The system shall generate a master plan, compliance matrix, executive metrics and prioritized alignment backlog from repository evidence.", "Turn recovered decisions into immediate, low-bureaucracy value.", "src/aias_governance_assurance/orchestrator.py", "tests/test_gov000049_governance_assurance.py"),
        ],
        "baseline_hours": 12.0, "actual_hours": 5.5, "automated_hours": 4.0, "reused_assets": 6, "total_assets": 8,
        "kpi_classification": "REFERENCE_ENGINEERING_ESTIMATE", "kpi_warning": "Post-validation reference estimate; documentation coverage and decision evidence are measured directly from the repository.",
    },
    "AIPD-000001": {
        "folder": "aipd000001", "spec_id": "SPEC-910001", "title": "AIAS Productivity Dashboard",
        "purpose": "Provide a permanent evidence-based command panel for AIAS technological capital, productivity, maturity, governance, departments, risk and delivery flow.",
        "scope": "Repository metric aggregation, constitutional status, SDD coverage, documentation, testing, maturity, 45 percent KPI, digital-company capability map, risks, backlog and static interactive dashboard generation.",
        "arch": "ARCH-AIPD-000001", "adr": "ADR-AIPD-000001", "status": "VALIDATED",
        "requirements": [
            ("REQ-910001","Evidence aggregation","The dashboard shall derive metrics from ACE, compliance, documentation, test and roadmap evidence.","Prevent manually invented executive status.","src/aias_productivity_dashboard/collector.py","tests/test_aipd000001_productivity_dashboard.py"),
            ("REQ-910002","Maturity distinction","The dashboard shall distinguish reference-case capability from audited organizational maturity.","Prevent unsupported Level 5 claims.","src/aias_productivity_dashboard/model.py","tests/test_aipd000001_productivity_dashboard.py"),
            ("REQ-910003","Digital company map","The dashboard shall expose Constitution, standards, departments, virtual engineers, operating system, university, security, PMO, nervous system, SDD and knowledge system states.","Manage AIAS as a digital engineering company.","src/aias_productivity_dashboard/collector.py","tests/test_aipd000001_productivity_dashboard.py"),
            ("REQ-910004","Sustainable acceleration","The dashboard shall display classified KPI evidence and flag results below the constitutional 45 percent target.","Keep acceleration measurable and honest.","src/aias_productivity_dashboard/model.py","tests/test_aipd000001_productivity_dashboard.py"),
            ("REQ-910005","Permanent panel","The system shall generate a self-contained interactive HTML panel and machine-readable snapshot.","Deliver immediate value without requiring a server.","src/aias_productivity_dashboard/renderer.py","tests/test_aipd000001_productivity_dashboard.py"),
            ("REQ-910006","Reproducible release","The system shall provide CLI, tests, documentation, installer and checksum-protected release evidence.","Make the dashboard maintainable and deployable.","src/aias_productivity_dashboard/orchestrator.py","tests/test_aipd000001_productivity_dashboard.py"),
        ],
        "baseline_hours": 8.0,"actual_hours": 3.5,"automated_hours": 2.5,"reused_assets": 7,"total_assets": 9,
        "kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; dashboard runtime metrics remain separately evidence-classified.",
    },
    "AMIR-000001": {
        "folder":"amir000001","spec_id":"SPEC-920001","title":"AIAS Master Inventory and Roadmap",
        "purpose":"Create the canonical, dependency-ordered inventory of all recovered AIAS rules, systems, offices, capabilities, programs and future visions before integral materialization continues.",
        "scope":"Stable identifiers, classification, lifecycle state, evidence, dependencies, duplicate resolution, chronological waves, lighthouse-project contract and machine-readable release.",
        "arch":"ARCH-AMIR-000001","adr":"ADR-AMIR-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-920001","Canonical catalog","The system shall register every recovered concept with a stable identifier, classification, state and evidence.","Prevent omissions and conceptual ambiguity.","src/aias_master_inventory/catalog.py","tests/test_amir000001_master_inventory.py"),
            ("REQ-920002","State honesty","The system shall distinguish operational, partial, specified, planned, superseded and duplicate concepts.","Prevent roadmap ideas from being represented as completed.","src/aias_master_inventory/validator.py","tests/test_amir000001_master_inventory.py"),
            ("REQ-920003","Dependency order","The system shall produce an acyclic dependency graph and chronological execution waves.","Enable giant steps without unsafe sequencing.","src/aias_master_inventory/roadmap.py","tests/test_amir000001_master_inventory.py"),
            ("REQ-920004","Evidence reconciliation","The system shall reconcile declared states with repository paths and report unsupported declarations.","Keep the repository as authority.","src/aias_master_inventory/evidence.py","tests/test_amir000001_master_inventory.py"),
            ("REQ-920005","Lighthouse contract","The system shall define Project Lighthouse 001 as the permanent real consumer of institutional and engineering capabilities.","Prevent infrastructure without immediate engineering value.","src/aias_master_inventory/lighthouse.py","tests/test_amir000001_master_inventory.py"),
            ("REQ-920006","Auditable release","The system shall generate JSON, Markdown, dependency, roadmap and checksum-protected release artifacts.","Preserve the complete plan across conversations and decades.","src/aias_master_inventory/orchestrator.py","tests/test_amir000001_master_inventory.py"),
        ],
        "baseline_hours":16.0,"actual_hours":7.0,"automated_hours":5.5,"reused_assets":8,"total_assets":10,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; concept state and evidence reconciliation are measured from the repository.",
    },
    "LIGHTHOUSE-000001": {
        "folder":"lighthouse000001","spec_id":"SPEC-930001","title":"Project Lighthouse 001 Minimum Vertical Slice",
        "purpose":"Demonstrate immediate end-to-end engineering value on a reference building while AIAS continues maturing toward organizational Level 5.",
        "scope":"Reference brief, assumptions, conceptual model, foundation chain, calculations, drawings, quantities, descriptive report, golden-thread traceability and review-controlled technical dossier.",
        "arch":"ARCH-LIGHTHOUSE-000001","adr":"ADR-LIGHTHOUSE-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-930001","Project brief","The slice shall define project purpose, scope, assumptions, units and professional boundaries.","Establish a reproducible engineering problem.","src/aias_lighthouse_project/brief.py","tests/test_lighthouse000001_reference_building.py"),
            ("REQ-930002","Real engine consumption","The slice shall consume the validated ECP foundation calculation, checking, documentation, delivery and handover chain.","Ensure infrastructure has an immediate engineering consumer.","src/aias_lighthouse_project/orchestrator.py","tests/test_lighthouse000001_reference_building.py"),
            ("REQ-930003","Technical deliverables","The slice shall produce calculations, vector drawings, quantities, descriptive report and technical dossier evidence.","Materialize design value before Level 5.","src/aias_lighthouse_project/reporting.py","tests/test_lighthouse000001_reference_building.py"),
            ("REQ-930004","Golden thread","Every delivered artifact shall link need, requirement, assumption, knowledge, calculation, result, drawing, document and review state.","Provide end-to-end engineering traceability.","src/aias_lighthouse_project/traceability.py","tests/test_lighthouse000001_reference_building.py"),
            ("REQ-930005","Maturity and legal status","The slice shall distinguish reference capability from construction approval and require professional review.","Prevent unsafe use and unsupported maturity claims.","src/aias_lighthouse_project/validation.py","tests/test_lighthouse000001_reference_building.py"),
            ("REQ-930006","Reproducible release","The slice shall provide tests, CLI, documentation, installer, manifest, checksums and versioned release.","Make the project a permanent regression consumer.","src/aias_lighthouse_project/orchestrator.py","tests/test_lighthouse000001_reference_building.py"),
        ],
        "baseline_hours":20.0,"actual_hours":8.0,"automated_hours":6.0,"reused_assets":9,"total_assets":11,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference-slice estimate; not a construction-project labor audit.",
    },
    "FOUNDATION-ALIGN-001": {
        "folder":"foundation_align001","spec_id":"SPEC-940001","title":"AIAS Charter and Executable Architecture Handbook",
        "purpose":"Complete the missing institutional foundations with a canonical Charter and machine-verifiable architecture rules aligned to the Constitution and SDD.",
        "scope":"Mission, identity, values, authority, professional boundaries, architectural layers, dependency rules, public contracts, modularity, reversibility, evidence and contradiction validation.",
        "arch":"ARCH-FOUNDATION-ALIGN-001","adr":"ADR-FOUNDATION-ALIGN-001","status":"VALIDATED",
        "requirements":[
            ("REQ-940001","Canonical Charter","The system shall define why AIAS exists, its mission, scope, values, stakeholders, authority and professional boundaries.","Close the first missing foundational document.","engineering/aias/foundation/AIAS_CHARTER.json","tests/test_foundation_align001.py"),
            ("REQ-940002","Architecture Handbook","The system shall define executable layers, dependency direction, contracts, modularity, reversibility and integration rules.","Close the architecture-governance foundation.","engineering/aias/foundation/AIAS_ARCHITECTURE_HANDBOOK.json","tests/test_foundation_align001.py"),
            ("REQ-940003","Hierarchy","The system shall enforce Charter, Constitution, SDD, Handbook, program specification and generated-artifact authority order.","Prevent conflicting project truth.","src/aias_foundation_governance/hierarchy.py","tests/test_foundation_align001.py"),
            ("REQ-940004","Architecture validation","The system shall reject forbidden inward/outward dependencies and missing public contracts.","Make the handbook executable.","src/aias_foundation_governance/validator.py","tests/test_foundation_align001.py"),
            ("REQ-940005","Professional boundary","The foundations shall preserve legal, jurisdictional and licensed-professional responsibility.","Protect safe engineering use.","src/aias_foundation_governance/validator.py","tests/test_foundation_align001.py"),
            ("REQ-940006","Reproducible release","The system shall provide CLI, tests, documentation, installer, manifests and checksum-protected release.","Keep foundations deployable and auditable.","src/aias_foundation_governance/orchestrator.py","tests/test_foundation_align001.py"),
        ],
        "baseline_hours":10.0,"actual_hours":4.0,"automated_hours":3.0,"reused_assets":7,"total_assets":9,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; constitutional consistency and architecture rules are measured directly.",
    },
    "FOUNDATION-ALIGN-002": {
        "folder":"foundation_align002","spec_id":"SPEC-940002","title":"AIAS Engineering System and AES Standards Registry",
        "purpose":"Complete the institutional production system and make the initial AIAS Engineering Standards machine-verifiable.",
        "scope":"Operating loop, accountable offices, engineering-asset lifecycle, mandatory evidence, professional boundary, normative standards, verification and review cycles.",
        "arch":"ARCH-FOUNDATION-ALIGN-002","adr":"ADR-FOUNDATION-ALIGN-002","status":"VALIDATED",
        "requirements":[
            ("REQ-941001","Engineering operating system","The system shall define the observe-to-learn production loop, accountable offices and asset lifecycle.","Create a durable digital engineering company operating model.","engineering/aias/foundation/AIAS_ENGINEERING_SYSTEM.json","tests/test_foundation_align002.py"),
            ("REQ-941002","Mandatory evidence","Every engineering asset lifecycle shall require specification, design, verification, release and feedback evidence.","Prevent unsupported completion claims.","engineering/aias/foundation/AIAS_ENGINEERING_SYSTEM.json","tests/test_foundation_align002.py"),
            ("REQ-941003","AES registry","The system shall maintain versioned standards with owners, normative rules, verification and review cycles.","Make standards governable and auditable.","engineering/aias/foundation/AIAS_AES_STANDARDS_REGISTRY.json","tests/test_foundation_align002.py"),
            ("REQ-941004","Executable validation","The system shall reject incomplete, duplicated, unowned or unverifiable standards.","Turn governance into an executable control.","src/aias_engineering_system/validator.py","tests/test_foundation_align002.py"),
            ("REQ-941005","Professional boundary","The system shall reserve regulated approval for the responsible licensed professional.","Preserve legal responsibility.","engineering/aias/foundation/AIAS_ENGINEERING_SYSTEM.json","tests/test_foundation_align002.py"),
            ("REQ-941006","Reproducible distribution","The system shall provide tests, documentation, manifest, checksums and installer.","Keep the foundation deployable.","scripts/build_foundation_align002_installer.py","tests/test_foundation_align002.py"),
        ],
        "baseline_hours":12.0,"actual_hours":5.0,"automated_hours":3.5,"reused_assets":8,"total_assets":10,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; operating-model adoption requires future production evidence.",
    },
    "ASSET-REGISTRY-001": {
        "folder":"asset_registry001","spec_id":"SPEC-950001","title":"Universal Engineering Asset Registry",
        "purpose":"Provide the canonical persistent identity, lifecycle and evidence registry for every AIAS engineering asset.",
        "scope":"Stable IDs, semantic versions, lifecycle transitions, dependencies, requirements, evidence, legal status, atomic persistence, audit events and queries.",
        "arch":"ARCH-ASSET-REGISTRY-001","adr":"ADR-ASSET-REGISTRY-001","status":"VALIDATED",
        "requirements":[
            ("REQ-950001","Universal asset contract","Every asset shall expose canonical identity, ownership, purpose, scope, source, requirements, evidence, dependencies and legal status.","Create one governable asset language.","engineering/aias/foundation/ENGINEERING_ASSET_SCHEMA.json","tests/test_asset_registry001.py"),
            ("REQ-950002","Persistent registry","The registry shall persist assets atomically and reject duplicate identities.","Protect registry consistency.","src/aias_asset_registry/registry.py","tests/test_asset_registry001.py"),
            ("REQ-950003","Dependency integrity","The registry shall reject references to unknown dependencies.","Preserve a valid asset graph.","src/aias_asset_registry/registry.py","tests/test_asset_registry001.py"),
            ("REQ-950004","Controlled lifecycle","Lifecycle transitions shall be sequential and auditable.","Prevent unsupported maturity claims.","src/aias_asset_registry/registry.py","tests/test_asset_registry001.py"),
            ("REQ-950005","Evidence queries","Consumers shall query assets by type and lifecycle state.","Enable ACE, Dashboard and PMO consumers.","src/aias_asset_registry/registry.py","tests/test_asset_registry001.py"),
            ("REQ-950006","Reproducible delivery","The capability shall include tests, documentation, installer and checksum release.","Make the registry deployable.","scripts/build_asset_registry001_installer.py","tests/test_asset_registry001.py")
        ],
        "baseline_hours":16.0,"actual_hours":7.0,"automated_hours":5.0,"reused_assets":8,"total_assets":10,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; operational scale requires continued registry ingestion evidence."
    },
    "DOC-ALIGN-002": {
        "folder":"doc_align002","spec_id":"SPEC-960002","title":"Complete Risk-Prioritized Public API Documentation",
        "purpose":"Eliminate measured documentation debt across all AIAS Python packages and prevent future drift.",
        "scope":"Modules, public functions, public classes, public methods, risk prioritization, semantic alignment, regression validation and executable coverage gate.",
        "arch":"ARCH-DOC-ALIGN-002","adr":"ADR-DOC-ALIGN-002","status":"VALIDATED",
        "requirements":[
            ("REQ-960201","Complete API scope","The audit shall include modules, public functions, classes and methods.","Prevent false coverage claims that omit methods.","src/aias_governance_assurance/documentation.py","tests/test_gov000049_governance_assurance.py"),
            ("REQ-960202","Risk prioritization","Documentation shall be completed in deterministic risk-first order.","Protect engineering-critical packages first.","src/aias_documentation_program/planner.py","tests/test_doc_align002.py"),
            ("REQ-960203","Zero measured debt","Every current AIAS module and public symbol shall contain semantic documentation.","Close the recovered documentation decision fully.","src","tests/test_doc_align002.py"),
            ("REQ-960204","Drift prevention","Repository validation shall fail when a new undocumented public API appears.","Keep documentation complete as AIAS grows.","tests/test_doc_align002.py","tests/test_doc_align002.py"),
            ("REQ-960205","Behavior preservation","Affected packages shall pass their functional regression suites.","Ensure documentation changes do not alter engineering behavior.","docs/DOC_ALIGN_002_COMPLETE_PUBLIC_API.md","tests/test_doc_align002.py"),
            ("REQ-960206","Reproducible delivery","The alignment shall include documentation, tests, installer, manifest, checksums and release.","Make the completed baseline deployable.","scripts/build_doc_align002_installer.py","tests/test_doc_align002.py")
        ],
        "baseline_hours":80.0,"actual_hours":32.0,"automated_hours":21.0,"reused_assets":20,"total_assets":24,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; coverage counts and regression outcomes are measured directly."
    },
    "ATO-000002": {
        "folder":"ato000002","spec_id":"SPEC-970002","title":"Continuous Technology Observatory",
        "purpose":"Continuously identify authoritative technologies and convert material opportunities into governed, actionable AIAS recommendations.",
        "scope":"Authorized sources, secure host validation, cadence, injected fetching, deduplication, scoring, radar, persistent cycles, AEC-000050 recommendations and ACE consumption.",
        "arch":"ARCH-ATO-000002","adr":"ADR-ATO-000002","status":"VALIDATED",
        "requirements":[
            ("REQ-970201","Authorized sources","The observatory shall poll only approved HTTPS source hosts with explicit cadence and evidence strength.","Control provenance and external attack surface.","engineering/aias/ato/ATO_CONTINUOUS_SOURCE_REGISTRY.json","tests/test_ato000002_continuous_observatory.py"),
            ("REQ-970202","Continuous cycles","The observatory shall determine due sources and persist cycle execution evidence.","Turn observation into a durable operating loop.","src/aias_continuous_observatory/engine.py","tests/test_ato000002_continuous_observatory.py"),
            ("REQ-970203","Deduplication","Repeated observations shall not create duplicate opportunities or recommendations.","Suppress non-actionable noise under AEC-000050.","src/aias_continuous_observatory/models.py","tests/test_ato000002_continuous_observatory.py"),
            ("REQ-970204","Technology radar","Admitted observations shall receive reproducible scoring and radar classification.","Support evidence-based portfolio decisions.","src/aias_continuous_observatory/engine.py","tests/test_ato000002_continuous_observatory.py"),
            ("REQ-970205","Strategic recommendation","Giant-step observations shall emit the complete AEC-000050 recommendation content.","Communicate material opportunities immediately.","src/aias_continuous_observatory/engine.py","tests/test_ato000002_continuous_observatory.py"),
            ("REQ-970206","Reproducible delivery","ATO shall include tests, documentation, installer, manifest, checksums and release.","Keep the observatory deployable.","scripts/build_ato000002_installer.py","tests/test_ato000002_continuous_observatory.py")
        ],
        "baseline_hours":24.0,"actual_hours":10.0,"automated_hours":7.0,"reused_assets":9,"total_assets":11,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; live-source operational uptime requires production monitoring evidence."
    },
    "UNIVERSITY-FOUNDATION-001": {
        "folder":"university_foundation001","spec_id":"SPEC-980001","title":"AIAS University Foundation",
        "purpose":"Build a capability-linked learning system that transfers AIAS knowledge without misrepresenting professional authority.",
        "scope":"Catalog, modules, lessons, canonical resources, progress, assessments, eligibility, identity verification, internal credentials and tamper verification.",
        "arch":"ARCH-UNIVERSITY-FOUNDATION-001","adr":"ADR-UNIVERSITY-FOUNDATION-001","status":"VALIDATED",
        "requirements":[
            ("REQ-980101","Capability-linked curriculum","Every course shall link to governed AIAS capability assets and canonical resources.","Keep learning synchronized with the real platform.","engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json","tests/test_university_foundation001.py"),
            ("REQ-980102","Structured content","Courses shall contain versioned modules, lessons and resource kinds.","Support tutorials, manuals and guided learning.","src/aias_university/catalog.py","tests/test_university_foundation001.py"),
            ("REQ-980103","Controlled assessment","Assessment shall require completed content, complete answers and a defined passing threshold.","Make competency evidence reproducible.","src/aias_university/engine.py","tests/test_university_foundation001.py"),
            ("REQ-980104","Verifiable credential","Eligible identity-verified learners shall receive tamper-evident credentials.","Provide machine-verifiable internal achievement evidence.","src/aias_university/credentials.py","tests/test_university_foundation001.py"),
            ("REQ-980105","Professional boundary","Credentials shall state that they are not professional licenses.","Prevent unsafe or legally misleading use.","engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json","tests/test_university_foundation001.py"),
            ("REQ-980106","Reproducible delivery","The university foundation shall include tests, documentation, installer, manifest, checksums and release.","Keep the subsystem deployable.","scripts/build_university_foundation001_installer.py","tests/test_university_foundation001.py")
        ],
        "baseline_hours":20.0,"actual_hours":8.0,"automated_hours":5.5,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; learning effectiveness requires future cohort evidence."
    },
    "CNS-000001": {
        "folder":"cns000001","spec_id":"SPEC-990001","title":"AIAS Central Nervous System",
        "purpose":"Provide durable, traceable and failure-aware circulation between the digital engineering company's core systems.",
        "scope":"Topology, immutable events, global sequence, atomic journal, event identity idempotency, subscriptions, cursors, dead letters and executive projections.",
        "arch":"ARCH-CNS-000001","adr":"ADR-CNS-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-990101","CNS topology","The system shall define producers, consumers and event contracts for core AIAS nodes.","Make company-system relationships explicit.","engineering/aias/cns/AIAS_CNS_TOPOLOGY.json","tests/test_cns000001.py"),
            ("REQ-990102","Durable event envelope","Accepted events shall be immutable, validated, sequenced and persisted before delivery.","Prevent lost or ambiguous state changes.","src/aias_central_nervous_system/models.py","tests/test_cns000001.py"),
            ("REQ-990103","Idempotency and ordering","Repeated event identities shall not duplicate journal entries and consumers shall receive sequence order.","Support reliable at-least-once circulation.","src/aias_central_nervous_system/journal.py","tests/test_cns000001.py"),
            ("REQ-990104","Consumer recovery","Consumers shall retain monotonic cursors and failed delivery evidence.","Enable replay and fault diagnosis.","src/aias_central_nervous_system/bus.py","tests/test_cns000001.py"),
            ("REQ-990105","Company projection","The system shall project delivery, recommendation, risk and credential state.","Give Dashboard and PMO an immediate CNS consumer.","src/aias_central_nervous_system/projection.py","tests/test_cns000001.py"),
            ("REQ-990106","Reproducible delivery","CNS shall include tests, documentation, installer, manifest, checksums and release.","Keep the nervous system deployable.","scripts/build_cns000001_installer.py","tests/test_cns000001.py")
        ],
        "baseline_hours":24.0,"actual_hours":10.0,"automated_hours":7.5,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; distributed production throughput requires future operational evidence."
    },
    "PMO-000001": {
        "folder":"pmo000001","spec_id":"SPEC-991001","title":"AIAS Portfolio Management Office",
        "purpose":"Select dependency-ready macro-deliveries and govern their evidence, benefits and closure.",
        "scope":"Portfolio records, scoring, dependencies, sequential stage gates, evidence, master-inventory ingestion and classified benefits realization.",
        "arch":"ARCH-PMO-000001","adr":"ADR-PMO-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-991101","Portfolio policy","PMO shall define stages, gate evidence, scoring weights and the acceleration target.","Create one executable portfolio authority.","engineering/aias/pmo/PMO_POLICY.json","tests/test_pmo000001.py"),
            ("REQ-991102","Dependency selection","Only proposed items with completed dependencies shall be selectable.","Preserve roadmap order and architectural prerequisites.","src/aias_pmo/portfolio.py","tests/test_pmo000001.py"),
            ("REQ-991103","Value prioritization","Candidates shall be scored by strategic value, urgency, reuse, acceleration, compliance, risk and effort.","Choose the greatest governed next step.","src/aias_pmo/portfolio.py","tests/test_pmo000001.py"),
            ("REQ-991104","Evidence gates","Portfolio stages shall advance sequentially only with target-stage evidence.","Prevent premature completion claims.","src/aias_pmo/portfolio.py","tests/test_pmo000001.py"),
            ("REQ-991105","Benefits realization","Time reduction shall be classified and checked against 45 percent.","Measure sustainable value honestly.","src/aias_pmo/portfolio.py","tests/test_pmo000001.py"),
            ("REQ-991106","Reproducible delivery","PMO shall include tests, documentation, installer, manifest, checksums and release.","Keep the office deployable.","scripts/build_pmo000001_installer.py","tests/test_pmo000001.py")
        ],
        "baseline_hours":18.0,"actual_hours":7.0,"automated_hours":5.0,"reused_assets":9,"total_assets":11,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; portfolio benefit outcomes require continued production measurement."
    },
    "AEKS-ALIGN-001": {
        "folder":"aeks_align001","spec_id":"SPEC-992001","title":"Executable Engineering Knowledge System Completion",
        "purpose":"Complete AEKS with safely executable, licensed, attributable and evidence-producing engineering knowledge.",
        "scope":"Admission, licenses, provenance, declarative expressions, AST allowlist, exact inputs, validation rules, units, hashes and professional review boundaries.",
        "arch":"ARCH-AEKS-ALIGN-001","adr":"ADR-AEKS-ALIGN-001","status":"VALIDATED",
        "requirements":[
            ("REQ-992101","Knowledge admission","Approved executable knowledge shall include license, provenance, deterministic mode and review boundary.","Protect lawful and safe knowledge use.","src/aias_executable_knowledge/admission.py","tests/test_aeks_align001.py"),
            ("REQ-992102","Safe execution","The executor shall allow arithmetic and comparisons while rejecting calls, attributes and unknown names.","Prevent knowledge payloads from executing arbitrary code.","src/aias_executable_knowledge/executor.py","tests/test_aeks_align001.py"),
            ("REQ-992103","Input contract","Inputs shall exactly match declared names, be finite and pass validation rules.","Make calculations deterministic and auditable.","src/aias_executable_knowledge/executor.py","tests/test_aeks_align001.py"),
            ("REQ-992104","Execution evidence","Results shall record knowledge version, units, jurisdiction, review status and integrity hashes.","Preserve the engineering golden thread.","src/aias_executable_knowledge/executor.py","tests/test_aeks_align001.py"),
            ("REQ-992105","Immediate consumer","A reference bearing-pressure EKU shall execute through the new boundary.","Materialize value under AEC-000049.","engineering/aias/aeks/EKU-000002-bearing-pressure.json","tests/test_aeks_align001.py"),
            ("REQ-992106","Reproducible delivery","AEKS alignment shall include tests, documentation, installer, manifest, checksums and release.","Keep executable knowledge deployable.","scripts/build_aeks_align001_installer.py","tests/test_aeks_align001.py")
        ],
        "baseline_hours":20.0,"actual_hours":8.0,"automated_hours":5.5,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; jurisdictional knowledge packs require separate licensed validation."
    },
    "EKG-000001": {
        "folder":"ekg000001","spec_id":"SPEC-993001","title":"AIAS Enterprise Knowledge Graph",
        "purpose":"Materialize the persistent, attributable and queryable golden thread for all AIAS enterprise knowledge.",
        "scope":"Typed nodes and edges, stable identity, versions, temporal metadata, atomic persistence, traversal, impact analysis, controlled inference and AMIR ingestion.",
        "arch":"ARCH-EKG-000001","adr":"ADR-EKG-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-993101","Canonical schema","Nodes and edges shall use stable typed identities, versions and source provenance.","Keep enterprise knowledge attributable and interoperable.","engineering/aias/ekg/EKG_SCHEMA.json","tests/test_ekg000001.py"),
            ("REQ-993102","Durable integrity","Persistence shall be atomic and reject identity conflicts and unknown endpoints.","Protect the enterprise golden thread.","src/aias_enterprise_knowledge_graph/graph.py","tests/test_ekg000001.py"),
            ("REQ-993103","Graph queries","EKG shall expose adjacency, directed paths and transitive impact.","Support dependency and change reasoning.","src/aias_enterprise_knowledge_graph/graph.py","tests/test_ekg000001.py"),
            ("REQ-993104","Controlled inference","Only explicitly approved rules may infer edges and every result shall retain supporting provenance.","Prevent unaudited semantic conclusions.","src/aias_enterprise_knowledge_graph/rules.py","tests/test_ekg000001.py"),
            ("REQ-993105","Immediate consumer","The complete AMIR inventory and dependency network shall import through EKG.","Materialize value under AEC-000049.","src/aias_enterprise_knowledge_graph/bootstrap.py","tests/test_ekg000001.py"),
            ("REQ-993106","Reproducible delivery","EKG shall include tests, documentation, installer, manifest, checksums and release.","Keep the graph deployable.","scripts/build_ekg000001_installer.py","tests/test_ekg000001.py")
        ],
        "baseline_hours":24.0,"actual_hours":9.0,"automated_hours":6.5,"reused_assets":11,"total_assets":13,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; production graph scale and query latency require operational telemetry."
    },
    "DEV-PLATFORM-001": {
        "folder":"dev_platform001","spec_id":"SPEC-993501","title":"Unified AIAS Development Platform",
        "purpose":"Expose verified AEPS generations through one governed, specification-driven and evidence-producing production boundary.",
        "scope":"Stable job/result contracts, isolated workspaces, least-complex engine selection, V3/V4/V5 adapters, normalized evidence, lifecycle events and tamper-evident records.",
        "arch":"ARCH-DEV-PLATFORM-001","adr":"ADR-DEV-PLATFORM-001","status":"VALIDATED",
        "requirements":[
            ("REQ-993501","Unified contract","Development jobs and results shall remain stable across AEPS engine generations.","Decouple consumers from production-engine evolution.","src/aias_development_platform/contracts.py","tests/test_dev_platform001.py"),
            ("REQ-993502","Governed selection","The platform shall select the least complex capable engine or honor an explicit supported mode.","Control complexity and preserve explainability.","src/aias_development_platform/policy.py","tests/test_dev_platform001.py"),
            ("REQ-993503","Safety boundary","Every run shall require specification identity, correlation and a workspace below the allowed root.","Prevent ambiguous or unsafe production runs.","src/aias_development_platform/policy.py","tests/test_dev_platform001.py"),
            ("REQ-993504","Evidence normalization","Every engine result shall expose certification, artifacts and tamper-evident normalized evidence.","Maintain a comparable development golden thread.","src/aias_development_platform/platform.py","tests/test_dev_platform001.py"),
            ("REQ-993505","Immediate consumer","The real AEPS V3 engine shall execute and certify a specification through the unified platform.","Materialize value under AEC-000049.","src/aias_development_platform/adapters.py","tests/test_dev_platform001.py"),
            ("REQ-993506","Reproducible delivery","The platform shall include tests, documentation, installer, checksums and release.","Keep the development control plane deployable.","scripts/build_dev_platform001_installer.py","tests/test_dev_platform001.py")
        ],
        "baseline_hours":28.0,"actual_hours":10.0,"automated_hours":7.5,"reused_assets":14,"total_assets":16,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; production throughput requires longitudinal operational evidence."
    },
    "CAPABILITY-FACTORY-001": {
        "folder":"capability_factory001","spec_id":"SPEC-993801","title":"Governed AIAS Capability Factory",
        "purpose":"Turn approved blueprints into registered, certified and reusable AIAS capabilities through the unified Development Platform.",
        "scope":"Blueprint contracts, atomic registry, immutable identity, sequential evidence gates, specification compilation, development delegation, validation, releases and lifecycle events.",
        "arch":"ARCH-CAPABILITY-FACTORY-001","adr":"ADR-CAPABILITY-FACTORY-001","status":"VALIDATED",
        "requirements":[
            ("REQ-993801","Blueprint contract","Capabilities shall declare identity, owner, approval, requirements, architecture and ADR references.","Make capability intent complete and reviewable.","src/aias_capability_factory/models.py","tests/test_capability_factory001.py"),
            ("REQ-993802","Lifecycle gates","Only sequential DRAFT through RELEASED transitions with target evidence shall be accepted.","Prevent premature capability claims.","src/aias_capability_factory/registry.py","tests/test_capability_factory001.py"),
            ("REQ-993803","Immutable registry","Stable capability identities shall reject conflicting blueprint replacement and persist atomically.","Protect reusable capability history.","src/aias_capability_factory/registry.py","tests/test_capability_factory001.py"),
            ("REQ-993804","Governed production","The factory shall compile a specification and delegate production to DEV-PLATFORM-001.","Reuse the certified production control plane.","src/aias_capability_factory/factory.py","tests/test_capability_factory001.py"),
            ("REQ-993805","Immediate consumer","A reference BIM wall-schedule capability shall reach RELEASED through the real Development Platform.","Materialize value under AEC-000049.","src/aias_capability_factory/factory.py","tests/test_capability_factory001.py"),
            ("REQ-993806","Reproducible delivery","The factory shall include tests, documentation, installer, checksums and release.","Keep the capability lifecycle deployable.","scripts/build_capability_factory001_installer.py","tests/test_capability_factory001.py")
        ],
        "baseline_hours":24.0,"actual_hours":8.0,"automated_hours":6.0,"reused_assets":13,"total_assets":15,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; realized reuse savings require production portfolio telemetry."
    },
    "SECURITY-RECOVERY-001": {
        "folder":"security_recovery001","spec_id":"SPEC-994001","title":"AIAS Security and Recovery System",
        "purpose":"Protect governed AIAS assets and prove that verified backups can be safely restored within declared recovery objectives.",
        "scope":"Secret detection and exclusion, signed manifests, per-file integrity, safe restoration, automated recovery drills, RPO/RTO measurement and non-destructive retention planning.",
        "arch":"ARCH-SECURITY-RECOVERY-001","adr":"ADR-SECURITY-RECOVERY-001","status":"VALIDATED",
        "requirements":[
            ("REQ-994001","Security exclusion","Backups shall exclude forbidden secrets, key files, symbolic links and detected embedded credentials without disclosing values.","Prevent sensitive-data propagation.","src/aias_security_recovery/scanner.py","tests/test_security_recovery001.py"),
            ("REQ-994002","Signed integrity","Every snapshot shall carry a caller-keyed HMAC manifest and SHA-256 digest for every included file.","Prove authenticity and integrity.","src/aias_security_recovery/backup.py","tests/test_security_recovery001.py"),
            ("REQ-994003","Safe restoration","Only verified safe members shall restore into an empty destination.","Prevent traversal and destructive overwrite.","src/aias_security_recovery/backup.py","tests/test_security_recovery001.py"),
            ("REQ-994004","Recovery objectives","RPO and RTO shall be explicit and evaluated from measured evidence.","Make recoverability operationally measurable.","src/aias_security_recovery/policy.py","tests/test_security_recovery001.py"),
            ("REQ-994005","Immediate consumer","A complete signed snapshot and automated restore drill shall recover reference AIAS project data.","Materialize HIST-013 and AEC-000049.","src/aias_security_recovery/backup.py","tests/test_security_recovery001.py"),
            ("REQ-994006","Reproducible delivery","Security and recovery shall include tests, documentation, installer, checksums and release.","Keep recoverability deployable.","scripts/build_security_recovery001_installer.py","tests/test_security_recovery001.py")
        ],
        "baseline_hours":30.0,"actual_hours":11.0,"automated_hours":8.0,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; production RPO/RTO compliance requires scheduled drills and external storage telemetry."
    },
    "OFFICES-FOUNDATION-001": {
        "folder":"offices_foundation001","spec_id":"SPEC-994501","title":"Dependency-Ready AIAS Enterprise Offices",
        "purpose":"Institutionalize accountable enterprise offices as executable charters without claiming offices whose dependencies are unavailable.",
        "scope":"Ten dependency-ready office charters, atomic registry, unique accountability routing, decision authorization, evidence gates, KPIs, escalation and explicit AI Office deferral.",
        "arch":"ARCH-OFFICES-FOUNDATION-001","adr":"ADR-OFFICES-FOUNDATION-001","status":"VALIDATED",
        "requirements":[
            ("REQ-994501","Complete charters","Each active office shall declare mandate, accountability, decision rights, evidence, KPIs and escalation.","Make organizational authority executable.","engineering/aias/offices/ENTERPRISE_OFFICE_CHARTERS.json","tests/test_offices_foundation001.py"),
            ("REQ-994502","Dependency honesty","Offices with unavailable dependencies shall remain explicitly deferred.","Prevent false organizational maturity.","src/aias_enterprise_offices/bootstrap.py","tests/test_offices_foundation001.py"),
            ("REQ-994503","Unique accountability","Work items shall route to exactly one accountable office.","Eliminate ownership ambiguity.","src/aias_enterprise_offices/registry.py","tests/test_offices_foundation001.py"),
            ("REQ-994504","Decision control","The registry shall allow only charter-authorized roles with complete evidence to decide an assigned work item.","Preserve separation of duties and auditability.","src/aias_enterprise_offices/registry.py","tests/test_offices_foundation001.py"),
            ("REQ-994505","Immediate consumers","Security recovery and capability automation work shall route through their real accountable offices.","Materialize institutional value under AEC-000049.","src/aias_enterprise_offices/registry.py","tests/test_offices_foundation001.py"),
            ("REQ-994506","Reproducible delivery","Office foundation shall include tests, documentation, installer, checksums and release.","Keep organizational governance deployable.","scripts/build_offices_foundation001_installer.py","tests/test_offices_foundation001.py")
        ],
        "baseline_hours":26.0,"actual_hours":9.0,"automated_hours":6.5,"reused_assets":12,"total_assets":14,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; organizational KPI outcomes require operational case history."
    },
    "ENGINEERING-WAVE12-001": {
        "folder":"engineering_wave12_001","spec_id":"SPEC-995001","title":"Dependency-Ready Engineering Capability Foundations",
        "purpose":"Close every roadmap-wave-12 engineering capability whose approved dependencies are operational while preserving regulated-use boundaries.",
        "scope":"Professional foundation workflow, jurisdiction registry, evidence ledger, differential validation, project reference library and explicit CAD/BIM deferral.",
        "arch":"ARCH-ENGINEERING-WAVE12-001","adr":"ADR-ENGINEERING-WAVE12-001","status":"VALIDATED",
        "requirements":[
            ("REQ-995001","Professional foundation workflow","The workflow shall execute validated calculation and code-check engines and join their releases in one evidence chain.","Deliver immediate professional engineering value.","src/aias_engineering_wave12/workflow.py","tests/test_engineering_wave12_001.py"),
            ("REQ-995002","Jurisdiction governance","Jurisdiction packs shall be licensed, attributable, effective-date-aware and explicit about legal status and review.","Prevent unauthorized regulatory claims.","src/aias_engineering_wave12/jurisdictions.py","tests/test_engineering_wave12_001.py"),
            ("REQ-995003","Evidence ledger","Engineering evidence shall be unique, attributable and linked through verifiable record hashes.","Protect the engineering golden thread.","src/aias_engineering_wave12/evidence.py","tests/test_engineering_wave12_001.py"),
            ("REQ-995004","Differential validation","Results shall compare exact contracts with matching units, provenance and explicit tolerances.","Detect controlled numerical regressions.","src/aias_engineering_wave12/differential.py","tests/test_engineering_wave12_001.py"),
            ("REQ-995005","Reference library","Reference cases shall be licensed, attributable, anonymized and identity-stable.","Enable reusable lawful validation.","src/aias_engineering_wave12/references.py","tests/test_engineering_wave12_001.py"),
            ("REQ-995006","Reproducible delivery","Wave 12 foundations shall include tests, documentation, installer, checksums and release.","Keep engineering assurance deployable.","scripts/build_engineering_wave12_001_installer.py","tests/test_engineering_wave12_001.py")
        ],
        "baseline_hours":38.0,"actual_hours":14.0,"automated_hours":10.5,"reused_assets":17,"total_assets":20,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; regulated project outcomes require jurisdiction packs and licensed professional approval."
    },
    "DRAWING-FRAMEWORK-001": {
        "folder":"drawing_framework001","spec_id":"SPEC-995501","title":"AIAS Enterprise Drawing Framework",
        "purpose":"Provide a canonical UI-independent engineering drawing model and deterministic portable vector outputs.",
        "scope":"Sheets, layers, lines, text, dimensions, views, scales, bounds, revisions, provenance, JSON, SVG, DXF, PDF, manifests and reference foundation sheet.",
        "arch":"ARCH-DRAWING-FRAMEWORK-001","adr":"ADR-DRAWING-FRAMEWORK-001","status":"VALIDATED",
        "requirements":[
            ("REQ-995501","Canonical drawing model","Drawings shall use stable entities, named layers, millimetre paper space, sheets, views, scales and provenance.","Enable interoperable engineering documentation.","src/aias_drawing_framework/models.py","tests/test_drawing_framework001.py"),
            ("REQ-995502","Drawing validation","The framework shall reject duplicate identity, unknown layers, unsafe text, invalid scales, out-of-bounds geometry and absent review boundaries.","Prevent malformed drawing releases.","src/aias_drawing_framework/validation.py","tests/test_drawing_framework001.py"),
            ("REQ-995503","Portable export","Validated drawings shall export deterministically to JSON, SVG, DXF and vector PDF.","Support CAD, browser, archive and printable consumers.","src/aias_drawing_framework/exporters.py","tests/test_drawing_framework001.py"),
            ("REQ-995504","Release evidence","Every exported format shall carry path, byte count and SHA-256 digest.","Make document artifacts auditable.","src/aias_drawing_framework/exporters.py","tests/test_drawing_framework001.py"),
            ("REQ-995505","Immediate consumer","A traceable A3 foundation plan shall render and preserve professional review status.","Materialize drawing value under AEC-000049.","src/aias_drawing_framework/reference.py","tests/test_drawing_framework001.py"),
            ("REQ-995506","Reproducible delivery","The framework shall include tests, documentation, installer, checksums and release.","Keep drawing production deployable.","scripts/build_drawing_framework001_installer.py","tests/test_drawing_framework001.py")
        ],
        "baseline_hours":32.0,"actual_hours":12.0,"automated_hours":9.0,"reused_assets":12,"total_assets":15,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; construction-document suitability requires discipline and jurisdiction-specific review."
    },
    "CAD-BIM-INTEGRATION-001": {
        "folder":"cad_bim_integration001","spec_id":"SPEC-995801","title":"Canonical AIAS CAD/BIM Integration",
        "purpose":"Bridge stable BIM elements into the Enterprise Drawing Framework with explicit units, mappings and semantic-loss evidence.",
        "scope":"Neutral interchange model, footprint projection, element-to-entity maps, loss reporting, JSON integrity, allowlisted property synchronization and Lighthouse consumer.",
        "arch":"ARCH-CAD-BIM-INTEGRATION-001","adr":"ADR-CAD-BIM-INTEGRATION-001","status":"VALIDATED",
        "requirements":[
            ("REQ-995801","Neutral contract","Interchange models shall use stable BIM identity, versions, millimetres and source provenance.","Create a controlled cross-domain boundary.","src/aias_cad_bim_integration/models.py","tests/test_cad_bim_integration001.py"),
            ("REQ-995802","Drawing projection","Supported BIM footprints shall map deterministically to canonical drawing entities.","Connect BIM semantics to portable drawings.","src/aias_cad_bim_integration/bridge.py","tests/test_cad_bim_integration001.py"),
            ("REQ-995803","Loss disclosure","Every unsupported semantic element shall appear in an explicit loss report.","Prevent silent interoperability loss.","src/aias_cad_bim_integration/bridge.py","tests/test_cad_bim_integration001.py"),
            ("REQ-995804","Controlled synchronization","Property updates shall be allowlisted, non-mutating and require transaction commit and professional review.","Protect BIM model authority.","src/aias_cad_bim_integration/bridge.py","tests/test_cad_bim_integration001.py"),
            ("REQ-995805","Immediate consumer","The Lighthouse BIM reference shall produce JSON, SVG, DXF and PDF drawings without undisclosed losses.","Materialize integration value under AEC-000049.","src/aias_cad_bim_integration/reference.py","tests/test_cad_bim_integration001.py"),
            ("REQ-995806","Reproducible delivery","CAD/BIM integration shall include tests, documentation, installer, checksums and release.","Keep interoperability deployable.","scripts/build_cad_bim_integration001_installer.py","tests/test_cad_bim_integration001.py")
        ],
        "baseline_hours":30.0,"actual_hours":11.0,"automated_hours":8.0,"reused_assets":14,"total_assets":17,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; complete IFC conformance and production authoring synchronization are not claimed."
    },
    "TECHNICAL-FILE-001": {
        "folder":"technical_file001","spec_id":"SPEC-996001","title":"AIAS Enterprise Technical File Generator",
        "purpose":"Assemble calculations, checks, drawings, narrative, coordination, custody and integrity evidence into one reviewable engineering dossier.",
        "scope":"Project brief, descriptive memory, professional foundation workflow, vector drawings, detailed documentation, transmittal, handover, integrity manifest, completeness and release.",
        "arch":"ARCH-TECHNICAL-FILE-001","adr":"ADR-TECHNICAL-FILE-001","status":"VALIDATED",
        "requirements":[
            ("REQ-996001","Technical dossier","The generator shall assemble all seven required dossier sections from operational engines.","Deliver a complete engineering technical file.","src/aias_technical_file/generator.py","tests/test_technical_file001.py"),
            ("REQ-996002","Descriptive memory","A structured descriptive memory shall be produced as JSON, Markdown and renderable PDF.","Provide human-readable project narrative.","src/aias_technical_file/memory.py","tests/test_technical_file001.py"),
            ("REQ-996003","Golden thread","Calculations, checks, drawings, documentation, revision, transmittal and custody shall remain linked in the package.","Preserve end-to-end traceability.","src/aias_technical_file/generator.py","tests/test_technical_file001.py"),
            ("REQ-996004","Integrity and completeness","Every file shall carry SHA-256 evidence and every required section shall be checked.","Make the dossier independently verifiable.","src/aias_technical_file/generator.py","tests/test_technical_file001.py"),
            ("REQ-996005","Professional boundary","The reference dossier shall remain FOR_REVIEW until official jurisdiction and licensed professional approvals exist.","Prevent unauthorized construction use.","engineering/aias/technical_file/TECHNICAL_FILE_SCHEMA.json","tests/test_technical_file001.py"),
            ("REQ-996006","Reproducible delivery","Technical file generation shall include tests, documentation, installer, checksums and release.","Keep dossier production deployable.","scripts/build_technical_file001_installer.py","tests/test_technical_file001.py")
        ],
        "baseline_hours":42.0,"actual_hours":15.0,"automated_hours":11.5,"reused_assets":24,"total_assets":27,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; construction approval requires official jurisdiction evidence and licensed professional signature."
    },
    "VIRTUAL-ORG-001": {
        "folder":"virtual_org001","spec_id":"SPEC-996501","title":"AIAS Virtual Engineering Organization",
        "purpose":"Operate a bounded, competent and auditable virtual engineering workforce without misrepresenting professional licensure.",
        "scope":"Roster, roles, offices, competencies, credentials, action authorization, work routing, evidence submission, independent review and human professional escalation.",
        "arch":"ARCH-VIRTUAL-ORG-001","adr":"ADR-VIRTUAL-ORG-001","status":"VALIDATED",
        "requirements":[
            ("REQ-996501","Governed roster","Every virtual engineer shall have stable identity, office, role, competency, authorized actions and credential references.","Make the virtual workforce accountable.","engineering/aias/virtual_organization/VIRTUAL_ENGINEER_ROSTER.json","tests/test_virtual_org001.py"),
            ("REQ-996502","No license claim","Virtual engineers shall never claim licensed-professional status.","Protect legal and ethical boundaries.","src/aias_virtual_organization/models.py","tests/test_virtual_org001.py"),
            ("REQ-996503","Qualified routing","Work shall route only to available engineers with all required competencies and action authority.","Prevent unqualified autonomous execution.","src/aias_virtual_organization/organization.py","tests/test_virtual_org001.py"),
            ("REQ-996504","Segregation of duties","The producing engineer and independent reviewer shall be different identities.","Preserve maker-checker control.","src/aias_virtual_organization/organization.py","tests/test_virtual_org001.py"),
            ("REQ-996505","Human final authority","High-risk or regulated work shall retain final authority with a licensed human professional.","Prevent unauthorized regulated approvals.","src/aias_virtual_organization/organization.py","tests/test_virtual_org001.py"),
            ("REQ-996506","Reproducible delivery","Virtual organization shall include tests, documentation, installer, checksums and release.","Keep workforce governance deployable.","scripts/build_virtual_org001_installer.py","tests/test_virtual_org001.py")
        ],
        "baseline_hours":28.0,"actual_hours":10.0,"automated_hours":7.5,"reused_assets":15,"total_assets":18,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; workforce performance requires operational work-order history and human oversight telemetry."
    },
    "INTELLIGENCE-CORE-001": {
        "folder":"intelligence_core001","spec_id":"SPEC-997001","title":"AIAS Engineering Intelligence Core",
        "purpose":"Produce bounded engineering recommendations from verified evidence with deterministic confidence, conflict detection and abstention.",
        "scope":"Requests, evidence identity, trust, claim coverage, risk thresholds, conflicts, recommendations, abstention, audit records, AEKS execution, differential validation and EKG context.",
        "arch":"ARCH-INTELLIGENCE-CORE-001","adr":"ADR-INTELLIGENCE-CORE-001","status":"VALIDATED",
        "requirements":[
            ("REQ-997001","Evidence contract","Every fact shall have identity, source, claim, value, trust, digest and legal status.","Prevent unsupported reasoning inputs.","src/aias_engineering_intelligence/models.py","tests/test_intelligence_core001.py"),
            ("REQ-997002","Deterministic confidence","Confidence shall derive from required-claim coverage, evidence trust, conflicts and risk threshold.","Make recommendation strength reproducible.","src/aias_engineering_intelligence/policy.py","tests/test_intelligence_core001.py"),
            ("REQ-997003","Mandatory abstention","The core shall abstain when claims are missing, contradictory or below the risk threshold.","Prevent invented or weak conclusions.","src/aias_engineering_intelligence/core.py","tests/test_intelligence_core001.py"),
            ("REQ-997004","Auditability","Every outcome shall retain evidence identifiers, reasons, assessment and record digest.","Preserve explainable decision lineage.","src/aias_engineering_intelligence/core.py","tests/test_intelligence_core001.py"),
            ("REQ-997005","Immediate consumer","A real AEKS calculation shall be checked by differential validation and EKG context before recommendation.","Materialize intelligence value under AEC-000049.","src/aias_engineering_intelligence/reference.py","tests/test_intelligence_core001.py"),
            ("REQ-997006","Reproducible delivery","Intelligence core shall include tests, documentation, installer, checksums and release.","Keep evidence intelligence deployable.","scripts/build_intelligence_core001_installer.py","tests/test_intelligence_core001.py")
        ],
        "baseline_hours":34.0,"actual_hours":12.0,"automated_hours":9.0,"reused_assets":16,"total_assets":19,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; production recommendation accuracy requires calibrated operational datasets and human outcome review."
    },
    "AI-OFFICE-001": {
        "folder":"ai_office001","spec_id":"SPEC-997501","title":"AIAS AI Office Activation",
        "purpose":"Activate accountable AI governance only after the Engineering Intelligence Core dependency is operational.",
        "scope":"Dependency gate, charter, intelligence-case routing, decision rights, model cards, evaluation, risk, oversight and KPI accountability.",
        "arch":"ARCH-AI-OFFICE-001","adr":"ADR-AI-OFFICE-001","status":"VALIDATED",
        "requirements":[
            ("REQ-997501","Dependency gate","AI Office shall activate only when SYS-000012 is operational.","Preserve institutional dependency integrity.","src/aias_enterprise_offices/ai_office.py","tests/test_ai_office001.py"),
            ("REQ-997502","Complete charter","AI Office shall declare mandate, accountability, decision rights, evidence, KPIs and escalation.","Make AI governance executable.","engineering/aias/offices/AI_OFFICE_CHARTER.json","tests/test_ai_office001.py"),
            ("REQ-997503","Case ownership","Engineering-intelligence governance cases shall route uniquely to AI Office.","Establish accountable oversight.","src/aias_enterprise_offices/ai_office.py","tests/test_ai_office001.py"),
            ("REQ-997504","Decision evidence","AI governance decisions shall require model card, evaluation, risk assessment and human oversight plan.","Prevent incomplete model approvals.","src/aias_enterprise_offices/registry.py","tests/test_ai_office001.py"),
            ("REQ-997505","Professional boundary","AI Office shall not grant licensed professional engineering approval.","Preserve human legal authority.","docs/AI_OFFICE001.md","tests/test_ai_office001.py"),
            ("REQ-997506","Reproducible delivery","AI Office activation shall include tests, documentation, installer, checksums and release.","Keep governance deployable.","scripts/build_ai_office001_installer.py","tests/test_ai_office001.py")
        ],
        "baseline_hours":14.0,"actual_hours":5.0,"automated_hours":3.5,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; governance effectiveness requires production model and override telemetry."
    },
    "AEOS-000001": {
        "folder":"aeos000001","spec_id":"SPEC-998001","title":"AIAS Engineering Operating System",
        "purpose":"Coordinate operational AIAS services through a dependency-aware, evidence-gated and event-driven project lifecycle.",
        "scope":"Service topology, health, project lifecycle, sequential gates, idempotent commands, correlation, evidence, audit hashes and CNS event integration.",
        "arch":"ARCH-AEOS-000001","adr":"ADR-AEOS-000001","status":"VALIDATED",
        "requirements":[
            ("REQ-998001","Service topology","AEOS shall register versioned capabilities, dependencies and explicit service health.","Make the digital company operationally observable.","src/aias_engineering_os/registry.py","tests/test_aeos000001.py"),
            ("REQ-998002","Lifecycle kernel","Projects shall advance sequentially from INITIATED through OPERATING.","Provide one governed operating lifecycle.","src/aias_engineering_os/kernel.py","tests/test_aeos000001.py"),
            ("REQ-998003","Evidence gates","Every target state shall require its service readiness and mandatory evidence.","Prevent unsupported operational claims.","src/aias_engineering_os/kernel.py","tests/test_aeos000001.py"),
            ("REQ-998004","Reliable commands","Commands shall be correlated, idempotent, atomically persisted and hash-audited.","Support safe retry and continuity.","src/aias_engineering_os/kernel.py","tests/test_aeos000001.py"),
            ("REQ-998005","Immediate consumer","The full Lighthouse lifecycle shall reach OPERATING and publish real CNS journal events.","Materialize operating-system value under AEC-000049.","tests/test_aeos000001.py","tests/test_aeos000001.py"),
            ("REQ-998006","Reproducible delivery","AEOS shall include tests, documentation, installer, checksums and release.","Keep the operating system deployable.","scripts/build_aeos000001_installer.py","tests/test_aeos000001.py")
        ],
        "baseline_hours":40.0,"actual_hours":14.0,"automated_hours":10.5,"reused_assets":21,"total_assets":24,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; production availability and recovery objectives require longitudinal service telemetry."
    },
    "AUTONOMOUS-CLOUD-001": {
        "folder":"autonomous_cloud001","spec_id":"SPEC-998501","title":"AIAS Cloud-Neutral Autonomous Engineering Control Plane",
        "purpose":"Materialize secure, recoverable and tenant-isolated autonomous engineering job control without unauthorized external provisioning.",
        "scope":"Tenants, principals, quotas, jobs, fair scheduling, trusted workers, leases, recovery, content-addressed artifacts, integrity and audit chain.",
        "arch":"ARCH-AUTONOMOUS-CLOUD-001","adr":"ADR-AUTONOMOUS-CLOUD-001","status":"VALIDATED",
        "requirements":[
            ("REQ-998501","Tenant isolation","Jobs and artifacts shall require tenant-scoped principal authorization and namespaces.","Prevent cross-tenant access.","src/aias_autonomous_cloud/control_plane.py","tests/test_autonomous_cloud001.py"),
            ("REQ-998502","Resource governance","Queued, running and artifact consumption shall respect explicit tenant quotas.","Bound cost and resource exhaustion.","src/aias_autonomous_cloud/models.py","tests/test_autonomous_cloud001.py"),
            ("REQ-998503","Reliable scheduling","Compatible jobs shall be fairly scheduled through trusted expiring worker leases and recoverable attempts.","Support autonomous resilient execution.","src/aias_autonomous_cloud/control_plane.py","tests/test_autonomous_cloud001.py"),
            ("REQ-998504","Artifact integrity","Artifacts shall be immutable, content-addressed, quota-bound and tenant-isolated.","Protect engineering output custody.","src/aias_autonomous_cloud/artifacts.py","tests/test_autonomous_cloud001.py"),
            ("REQ-998505","Immediate consumer","A Lighthouse AEOS operating job shall lease, store evidence and complete through the cloud-neutral control plane.","Materialize future value under AEC-000049.","tests/test_autonomous_cloud001.py","tests/test_autonomous_cloud001.py"),
            ("REQ-998506","Reproducible delivery","Cloud control plane shall include tests, documentation, installer, checksums and release.","Keep autonomous execution deployable.","scripts/build_autonomous_cloud001_installer.py","tests/test_autonomous_cloud001.py")
        ],
        "baseline_hours":38.0,"actual_hours":13.0,"automated_hours":9.5,"reused_assets":18,"total_assets":22,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; no external cloud infrastructure, cost, region, residency or production SLA is claimed."
    },
    "LEVEL5-ASSURANCE-001": {
        "folder":"level5_assurance001","spec_id":"SPEC-999001","title":"AIAS Level 5 Organizational Assurance System",
        "purpose":"Separate demonstrated reference capability from independently audited longitudinal organizational maturity.",
        "scope":"Systems, six criteria, evidence classifications, metrics, observation windows, project counts, critical findings, independent audit and explicit gaps.",
        "arch":"ARCH-LEVEL5-ASSURANCE-001","adr":"ADR-LEVEL5-ASSURANCE-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999001","Evidence classification","Assurance evidence shall distinguish reference validation, production observation and independent audit.","Prevent test evidence from masquerading as production maturity.","src/aias_level5_assurance/models.py","tests/test_level5_assurance001.py"),
            ("REQ-999002","Reference capability","Reference Level 5 shall require all designated systems and criterion validation evidence.","Measure technical mechanism availability honestly.","src/aias_level5_assurance/assessment.py","tests/test_level5_assurance001.py"),
            ("REQ-999003","Longitudinal maturity","Organizational Level 5 shall require at least 365 days, ten projects, production evidence and threshold metrics.","Require sustained organizational outcomes.","src/aias_level5_assurance/policy.py","tests/test_level5_assurance001.py"),
            ("REQ-999004","Independent audit","Organizational Level 5 shall require a conformant independent attestation with no critical findings.","Prohibit self-certification.","src/aias_level5_assurance/models.py","tests/test_level5_assurance001.py"),
            ("REQ-999005","Immediate consumer","Current AIAS evidence shall assess as reference Level 5 while organizational audited level remains null.","Publish an honest current maturity state.","src/aias_level5_assurance/reference.py","tests/test_level5_assurance001.py"),
            ("REQ-999006","Reproducible delivery","Level 5 assurance shall include tests, documentation, installer, checksums and release.","Keep maturity assurance deployable.","scripts/build_level5_assurance001_installer.py","tests/test_level5_assurance001.py")
        ],
        "baseline_hours":24.0,"actual_hours":8.0,"automated_hours":5.5,"reused_assets":14,"total_assets":17,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"The assurance mechanism is validated; AIAS organizational Level 5 remains unaudited pending longitudinal production evidence and independent audit."
    },
    "END-TO-END-001": {
        "folder":"end_to_end001","spec_id":"SPEC-999501","title":"AIAS End-to-End Project Production",
        "purpose":"Demonstrate the complete governed AIAS project chain from planning through operating custody on Lighthouse.",
        "scope":"PMO plan, virtual assignment, technical file, independent review, AEOS, CNS, signed recovery, cloud-neutral custody, release and professional boundary.",
        "arch":"ARCH-END-TO-END-001","adr":"ADR-END-TO-END-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999501","Complete chain","Production shall connect planning, assignment, generation, review, release, handover, operation, recovery and custody.","Prove system integration across the digital company.","src/aias_end_to_end/producer.py","tests/test_end_to_end001.py"),
            ("REQ-999502","Independent review","Author and virtual reviewer shall be different identities and regulated authority shall remain human.","Preserve professional maker-checker control.","src/aias_end_to_end/producer.py","tests/test_end_to_end001.py"),
            ("REQ-999503","Operating evidence","Lighthouse shall reach AEOS OPERATING with seven durable CNS lifecycle events.","Prove the operational lifecycle.","src/aias_end_to_end/producer.py","tests/test_end_to_end001.py"),
            ("REQ-999504","Resilience and custody","The final technical release shall pass a signed recovery drill and tenant-isolated cloud-neutral custody.","Protect project continuity and artifacts.","src/aias_end_to_end/producer.py","tests/test_end_to_end001.py"),
            ("REQ-999505","Honest status","The output shall remain reference-for-review and shall not claim professional approval or audited organizational Level 5.","Prevent unsupported completion claims.","engineering/aias/end_to_end/END_TO_END_CONTRACT.json","tests/test_end_to_end001.py"),
            ("REQ-999506","Reproducible delivery","End-to-end production shall include tests, documentation, installer, checksums and release.","Keep complete project production deployable.","scripts/build_end_to_end001_installer.py","tests/test_end_to_end001.py")
        ],
        "baseline_hours":60.0,"actual_hours":20.0,"automated_hours":15.0,"reused_assets":35,"total_assets":39,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Post-validation reference estimate; Lighthouse is a reference-for-review project, not an approved construction delivery or organizational maturity audit."
    },
    "LEVEL5-EVIDENCE-CAMPAIGN-001": {
        "folder":"level5_evidence_campaign001","spec_id":"SPEC-999601","title":"AIAS Level 5 Longitudinal Evidence Campaign",
        "purpose":"Capture authentic production observations over time without fabricating organizational maturity.",
        "scope":"Authenticated hash-chained ledger, project events, criteria, metrics, professional reviews, recovery, incidents, improvements, audit attestations, CLI and dashboard status.",
        "arch":"ARCH-LEVEL5-EVIDENCE-CAMPAIGN-001","adr":"ADR-LEVEL5-EVIDENCE-CAMPAIGN-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999601","Tamper-evident ledger","Every production record shall be sequenced, hash chained and authenticated with an externally supplied key.","Preserve longitudinal evidence integrity.","src/aias_level5_assurance/ledger.py","tests/test_level5_evidence_campaign001.py"),
            ("REQ-999602","Real observation controls","The campaign shall reject future observations, duplicates, missing sources and invalid normative dimensions.","Prevent fabricated or ambiguous maturity evidence.","src/aias_level5_assurance/ledger.py","tests/test_level5_evidence_campaign001.py"),
            ("REQ-999603","Honest progress","Campaign status shall derive window, unique completed projects, criteria and threshold metrics without prematurely claiming Level 5.","Keep capability and maturity claims separate.","src/aias_level5_assurance/ledger.py","tests/test_level5_evidence_campaign001.py"),
            ("REQ-999604","Assessor interoperability","Verified criterion observations shall project into production evidence accepted by the Level 5 assessor.","Connect collection to formal assessment.","src/aias_level5_assurance/ledger.py","tests/test_level5_evidence_campaign001.py"),
            ("REQ-999605","Secure operation","The CLI shall obtain its signing key externally and shall not embed production secrets.","Protect evidence authenticity and deployability.","src/aias_level5_assurance/cli.py","tests/test_level5_evidence_campaign001.py"),
            ("REQ-999606","Reproducible delivery","The campaign shall include specification, traceability, tests, documentation, installer, checksums and release.","Keep evidence collection maintainable.","scripts/build_level5_evidence_campaign001_installer.py","tests/test_level5_evidence_campaign001.py")
        ],
        "baseline_hours":28.0,"actual_hours":9.0,"automated_hours":6.5,"reused_assets":15,"total_assets":18,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"The evidence mechanism is validated; elapsed production time, project count and independent audit remain real-world observations only."
    },
    "CERTIFICATION-MASTER-PLAN-001": {
        "folder":"certification_master_plan001","spec_id":"SPEC-999701","title":"AIAS Certification Master Plan",
        "purpose":"Establish the official external maturity and certification architecture for AIAS without unsupported claims.",
        "scope":"CMMI-DEV V3.0 ML5, CMMI AIM, ISO 9001, ISO/IEC 27001, ISO/IEC 42001, ISO 22301, authorities, sequencing, version monitoring, evidence readiness and professional boundaries.",
        "arch":"ARCH-CERTIFICATION-MASTER-PLAN-001","adr":"ADR-CERTIFICATION-MASTER-PLAN-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999701","Official maturity objective","The program shall designate CMMI-DEV V3.0 Maturity Level 5 as the sole primary organizational maturity objective.","Prevent ambiguous or competing Level 5 claims.","src/aias_certification_program/registry.py","tests/test_certification_master_plan001.py"),
            ("REQ-999702","AI maturity and management","CMMI AIM shall be mandatory and ISO/IEC 42001 shall govern the certifiable AI management system.","Cover both AI maturity and responsible AI management.","engineering/aias/certification/AIAS_CERTIFICATION_MASTER_PLAN.json","tests/test_certification_master_plan001.py"),
            ("REQ-999703","Integrated management system","The plan shall target quality, information security, AI management and business continuity through ISO 9001, ISO/IEC 27001, ISO/IEC 42001 and ISO 22301.","Create a coherent certification portfolio.","src/aias_certification_program/registry.py","tests/test_certification_master_plan001.py"),
            ("REQ-999704","External authority boundary","AIAS shall not self-issue CMMI ratings, ISO certificates or professional engineering approvals.","Preserve legal and certification credibility.","engineering/aias/certification/AIAS_CERTIFICATION_MASTER_PLAN.json","tests/test_certification_master_plan001.py"),
            ("REQ-999705","Honest readiness","Internal evidence assessment shall never claim external conformity, certification or appraisal rating.","Separate preparation from independent decisions.","src/aias_certification_program/assessment.py","tests/test_certification_master_plan001.py"),
            ("REQ-999706","Version and copyright governance","The plan shall monitor normative revisions and shall not reproduce unlicensed standards or model content.","Keep the program current and lawful.","docs/CERTIFICATION_MASTER_PLAN001.md","tests/test_certification_master_plan001.py")
        ],
        "baseline_hours":32.0,"actual_hours":10.0,"automated_hours":6.5,"reused_assets":16,"total_assets":20,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"The plan and readiness mechanism are validated; no external certification or CMMI maturity rating is claimed."
    },
    "GOV-CONTINUITY-001": {
        "folder":"gov_continuity001","spec_id":"SPEC-999801","title":"AEC-000051 Verifiable Conversation Continuity",
        "purpose":"Guarantee repository-derived project resumption before replacing the primary AIAS conversation.",
        "scope":"Constitutional rule, ACE regeneration, mandatory evidence set, checksum-protected archive, tamper detection, CLI, policy and executive order.",
        "arch":"ARCH-GOV-CONTINUITY-001","adr":"ADR-GOV-CONTINUITY-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999801","Constitutional mandate","AEC-000051 shall require a validated continuity package before primary-conversation migration or replacement.","Make continuity durable and mandatory.","engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml","tests/test_aec000051_continuity_rule.py"),
            ("REQ-999802","Minimum evidence","The package shall contain master context, project state, next task, continuation prompt and executive orders.","Preserve sufficient restart authority.","src/aias_context_engine/continuity.py","tests/test_aec000051_continuity_rule.py"),
            ("REQ-999803","Integrity","Every content file and the archive shall have SHA-256 verification evidence.","Detect incomplete or altered handoffs.","src/aias_context_engine/continuity.py","tests/test_aec000051_continuity_rule.py"),
            ("REQ-999804","Repository authority","The handoff shall derive from validated ACE state rather than screenshots or narrative memory alone.","Prevent continuity loss after context compaction.","engineering/aias/master/CONVERSATION_CONTINUITY_POLICY.json","tests/test_aec000051_continuity_rule.py"),
            ("REQ-999805","Operational CLI","Operators shall be able to create and independently verify the handoff package through ACE CLI commands.","Make the rule executable.","src/aias_context_engine/cli.py","tests/test_aec000051_continuity_rule.py"),
            ("REQ-999806","Reproducible delivery","The rule shall include tests, policy, installer, checksums and release.","Keep continuity deployable.","scripts/build_gov_continuity001_installer.py","tests/test_aec000051_continuity_rule.py")
        ],
        "baseline_hours":18.0,"actual_hours":5.5,"automated_hours":4.0,"reused_assets":10,"total_assets":12,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"The mechanism is validated; a handoff package must still be regenerated immediately before each actual conversation transition."
    },
    "CERTIFICATION-IMS-FOUNDATION-001": {
        "folder":"certification_ims_foundation001","spec_id":"SPEC-999901","title":"AIAS Integrated Management System Foundation",
        "purpose":"Create one evidence-based management-system foundation for quality, information security, AI management and business continuity.",
        "scope":"Context, policy, ownership, risk, objectives, documented information, internal audit, management review, corrective action, high-level control families and external certification boundary.",
        "arch":"ARCH-CERTIFICATION-IMS-FOUNDATION-001","adr":"ADR-CERTIFICATION-IMS-FOUNDATION-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999901","Integrated foundation","One common system shall govern four management domains and approved ISO targets.","Avoid duplicated certification bureaucracy.","src/aias_integrated_management/system.py","tests/test_certification_ims_foundation001.py"),
            ("REQ-999902","Risk and objectives","The system shall maintain owned, scored risks and measurable objectives without invented observations.","Drive evidence-based management.","src/aias_integrated_management/models.py","tests/test_certification_ims_foundation001.py"),
            ("REQ-999903","Assurance cycle","The system shall support internal audits, management review and corrective actions with traceable evidence.","Institutionalize evaluation and improvement.","src/aias_integrated_management/system.py","tests/test_certification_ims_foundation001.py"),
            ("REQ-999904","No self-certification","Internal implementation and audits shall never authorize an external certification claim.","Preserve independent certification authority.","src/aias_integrated_management/system.py","tests/test_certification_ims_foundation001.py"),
            ("REQ-999905","Licensed content boundary","The system shall materialize only high-level common families until legitimate normative access is available for clause-level crosswalks.","Respect standards copyright and assessment accuracy.","engineering/aias/certification/IMS_FOUNDATION_POLICY.json","tests/test_certification_ims_foundation001.py"),
            ("REQ-999906","Immediate consumer","AIAS shall generate a real foundation state with four risks, four objectives, an audit program, management review and corrective action.","Deliver operational value immediately.","scripts/generate_ims_foundation_reference.py","tests/test_certification_ims_foundation001.py")
        ],
        "baseline_hours":46.0,"actual_hours":14.0,"automated_hours":9.5,"reused_assets":20,"total_assets":24,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"The integrated foundation is implemented; conformity to ISO clauses and external certification remain unclaimed pending legitimate normative access and independent audit."
    },
    "CERTIFICATION-NORMATIVE-ACCESS-001": {
        "folder":"certification_normative_access001","spec_id":"SPEC-999902","title":"AIAS Normative Access and External Assessment Readiness",
        "purpose":"Prepare lawful standards acquisition, certification scope and independent-provider evaluation without authorizing commercial action.",
        "scope":"Normative asset registry, copyright boundary, certification scope, provider competence, independence, RFP and human authorization gates.",
        "arch":"ARCH-CERTIFICATION-NORMATIVE-ACCESS-001","adr":"ADR-CERTIFICATION-NORMATIVE-ACCESS-001","status":"VALIDATED",
        "requirements":[
            ("REQ-999911","Legitimate access","AIAS shall inventory required normative assets and acquire them only through authorized channels.","Protect copyright and assessment accuracy.","src/aias_normative_access/registry.py","tests/test_certification_normative_access001.py"),
            ("REQ-999912","Certification scope","AIAS shall maintain a draft scope with explicit exclusions and external scoping gates.","Prevent unsupported scope claims.","src/aias_normative_access/scoping.py","tests/test_certification_normative_access001.py"),
            ("REQ-999913","Provider competence","Candidates shall have independently verifiable authority and framework-specific competence.","Select qualified external assurance.","src/aias_normative_access/vendors.py","tests/test_certification_normative_access001.py"),
            ("REQ-999914","Independence","Provider evaluation shall require independence and conflict disclosure.","Preserve assurance credibility.","src/aias_normative_access/vendors.py","tests/test_certification_normative_access001.py"),
            ("REQ-999915","Human authorization","No purchase, outreach, selection, contract or certification claim shall occur without explicit authorization.","Respect commercial and legal authority.","engineering/aias/certification/NORMATIVE_ACCESS_PLAN.json","tests/test_certification_normative_access001.py"),
            ("REQ-999916","Reproducible readiness","The capability shall include SDD, tests, documentation, installer, reference state and checksum release.","Keep certification preparation auditable.","scripts/build_certification_normative_access001_installer.py","tests/test_certification_normative_access001.py")
        ],
        "baseline_hours":24.0,"actual_hours":7.0,"automated_hours":5.0,"reused_assets":12,"total_assets":15,"kpi_classification":"REFERENCE_ENGINEERING_ESTIMATE","kpi_warning":"Procurement readiness is validated; no standards purchase, provider appointment, certification or maturity rating is claimed."
    },
}


def requirement(row, status=RequirementStatus.VALIDATED):
    req_id, title, statement, rationale, implementation, test = row
    return Requirement(req_id, title, statement, RequirementType.FUNCTIONAL, status, rationale, ["Implementation exists or is formally planned.", "Automated acceptance test is linked.", "Traceability link is present."], [implementation], [test])


def generate(component_id: str) -> dict:
    definition = DEFINITIONS[component_id]
    output = ROOT / "engineering" / definition["folder"] / "compliance"
    output.mkdir(parents=True, exist_ok=True)
    status = RequirementStatus(definition.get("status", "VALIDATED"))
    requirements = [requirement(row, status) for row in definition["requirements"]]
    spec = Specification(definition["spec_id"], definition["title"], "1.0.0", definition["purpose"], definition["scope"], requirements, [definition["arch"]], [definition["adr"]], ["Generated engineering output requires human review."])
    matrix = TraceabilityMatrix()
    for req in requirements:
        for implementation in req.implements:
            matrix.link(req.requirement_id, "implemented_by", implementation)
        for test in req.tested_by:
            matrix.link(req.requirement_id, "tested_by", test)
    gates = QualityGateEngine().evaluate(spec, matrix)
    kpi = ProductivitySnapshot(definition["baseline_hours"], definition["actual_hours"], definition["automated_hours"], definition["reused_assets"], definition["total_assets"])
    spec_row = asdict(spec)
    for req in spec_row["requirements"]:
        req["requirement_type"] = req["requirement_type"].value
        req["status"] = req["status"].value
    trace_row = {source: {relation: sorted(targets) for relation, targets in relations.items()} for source, relations in matrix.links.items()}
    report = {
        "component_id": component_id,
        "constitution": "AEC-000002",
        "articles": ["AEC-ART-000001", "AEC-ART-000002", "AEC-ART-000003", "AEC-ART-000004", "AEC-000049", "AEC-000050", "AEC-000051"],
        "gates": [asdict(gate) for gate in gates],
        "all_passed": all(gate.passed for gate in gates) and kpi.meets_acceleration_target,
        "kpi": {"classification": definition.get("kpi_classification", "REFERENCE_ENGINEERING_ESTIMATE"), "baseline_hours": kpi.baseline_hours, "actual_hours": kpi.actual_hours, "time_reduction": kpi.time_reduction, "automation_ratio": kpi.automation_ratio, "reuse_ratio": kpi.reuse_ratio, "meets_45_percent_target": kpi.meets_acceleration_target, "warning": definition.get("kpi_warning", "Reference productivity estimate; not an independently audited labor study.")},
        "validator_issues": SpecificationValidator().validate(spec),
    }
    (output / "ASDD.json").write_text(json.dumps(spec_row, indent=2) + "\n", encoding="utf-8")
    (output / "TRACEABILITY.json").write_text(json.dumps(trace_row, indent=2) + "\n", encoding="utf-8")
    (output / "QUALITY_GATES.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / f"{definition['adr']}.md").write_text(f"# {definition['adr']}\n\nStatus: Accepted\n\nDecision: implement {definition['title']} as a reusable platform capability governed by AEC-000002.\n\nConsequences: requirements, implementation, tests and release evidence remain traceable.\n", encoding="utf-8")
    (output / f"{definition['arch']}.md").write_text(f"# {definition['arch']}\n\nComponent: {component_id}\n\nPurpose: {definition['purpose']}\n\nArchitecture: modular Python package, CLI, automated validation, documentation and release evidence.\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("components", nargs="*", help="Component IDs; omit to regenerate every governed component.")
    args = parser.parse_args()
    components = args.components or sorted(DEFINITIONS)
    unknown = sorted(set(components) - set(DEFINITIONS))
    if unknown:
        parser.error(f"unknown components: {', '.join(unknown)}")
    reports = [generate(component) for component in components]
    print(json.dumps(reports, indent=2))
    return 0 if all(report["all_passed"] for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
