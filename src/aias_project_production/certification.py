"""Public certification API with explicit STRESS design-failure certification."""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .certification_legacy import *  # noqa: F401,F403 - preserve the existing certification API
from . import certification_legacy as _legacy


def _design_manifest(project_id: str, width: float, length: float, levels: int, scenario_id: str) -> dict:
    manifest = _legacy._manifest(project_id, width, length, levels)
    manifest["scenario_id"] = scenario_id
    return manifest


def _run_design_scenario(manifest: dict) -> tuple[object, dict]:
    from aias_project_intake.builders import ParametricProjectGraphBuilder
    from aias_structural_professional import ProfessionalStructuralEngine

    graph = ParametricProjectGraphBuilder().build(manifest)
    engine = ProfessionalStructuralEngine()
    model = engine.generate_3d_model(graph)
    engine.add_loads(model)
    if manifest["scenario_id"] == "STRESS_CASE_001":
        for load in model.loads:
            load["magnitude"] *= 30.0
    engine.apply_combinations(model)
    standards = {
        "pack": "AIAS-SYNTHETIC-ANALYSIS-001",
        "scenario_id": manifest["scenario_id"],
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
    }
    standards["pack_sha256"] = hashlib.sha256(
        json.dumps(standards, sort_keys=True).encode()
    ).hexdigest()
    return engine.analyze_and_design(model, standards), standards


def certify_design_production_core(output_root: str | Path) -> dict:
    """Certify one successful design and one intentional STRESS capacity failure.

    A STRESS capacity failure is a valid scenario outcome, not missing evidence.
    It must materialize evidence but must never materialize reinforcement.
    """
    from aias_reinforcement_detailing import ReinforcementEngine

    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifests = [
        _design_manifest("DESIGN-CORE-CERT-A", 8.0, 9.0, 2, "NOMINAL_CASE_001"),
        _design_manifest("DESIGN-CORE-CERT-B", 11.0, 7.0, 3, "STRESS_CASE_001"),
    ]
    projects = []
    deterministic = []
    scenario_faults = []

    for manifest in manifests:
        analysis, standards = _run_design_scenario(manifest)
        repeated_analysis, repeated_standards = _run_design_scenario(copy.deepcopy(manifest))
        analysis_sha = analysis.evidence_sha256
        standards_sha = analysis.analysis_trace.get("standards_evidence_sha256", "")
        scenario_id = manifest["scenario_id"]

        if scenario_id == "STRESS_CASE_001":
            capacity_failed = analysis.status == "FAIL" and any(
                check.get("status") == "FAIL" for check in analysis.design_checks.values()
            )
            if not capacity_failed:
                raise AssertionError("STRESS_CASE_001 must exceed structural design capacity")
            try:
                ReinforcementEngine().build(analysis, standards, project_id=manifest["project_id"])
            except ValueError as exc:
                if "DESIGN_CAPACITY_EXCEEDED" not in str(exc):
                    raise
            else:
                raise AssertionError("capacity failure must fail closed before reinforcement")

            fault = _legacy._synthetic_scenario_fault_evidence(
                manifest["project_id"], analysis_sha, standards_sha,
                "STRESS scenario: structural demand exceeded design capacity",
            )
            evidence = {
                "schema": "aias.design_project_evidence.v1",
                "project_id": manifest["project_id"],
                "scenario_id": scenario_id,
                "SYNTHETIC_TEST_DATA": True,
                "NOT_FOR_CONSTRUCTION": True,
                "classification": "SCENARIO_FAILURE_NOT_FOR_CONSTRUCTION",
                "reinforcement": None,
                "analysis_evidence_sha256": analysis_sha,
                "standards_evidence_sha256": standards_sha,
                "quantity_trace": None,
                "qa_reinforcement_trace": None,
                "scenario_fault_evidence": fault,
            }
            filename = f"{manifest['project_id']}_DESIGN_EVIDENCE_SCENARIO_FAULT.json"
            _legacy._write(output_root / filename, evidence)
            deterministic.append(
                repeated_analysis.evidence_sha256 == analysis.evidence_sha256
                and repeated_standards == standards
            )
            scenario_faults.append(manifest["project_id"])
            projects.append({
                "project_id": manifest["project_id"], "scenario_id": scenario_id,
                "evidence_file": filename, "evidence_sha256": _legacy._sha256(evidence),
                "design_evidence_sha256": fault["design_evidence_sha256"],
                "analysis_evidence_sha256": analysis_sha,
                "standards_evidence_sha256": standards_sha,
                "bar_set_count": 0, "steel_kg": 0,
                "status": "SCENARIO_FAILURE_DETECTED", "scenario_fault": True,
                "failure_reason": fault["failure_reason"],
                "no_invalid_design_output": (
                    evidence["reinforcement"] is None
                    and evidence["quantity_trace"] is None
                    and fault["bar_sets"] == [] and fault["schedules"] == []
                ),
            })
            continue

        if analysis.status != "PASS":
            raise AssertionError("nominal certification scenario must pass analysis")
        reinforcement = ReinforcementEngine().build(analysis, standards, project_id=manifest["project_id"])
        repeated = ReinforcementEngine().build(
            repeated_analysis, repeated_standards, project_id=manifest["project_id"]
        )
        deterministic.append(asdict(repeated) == asdict(reinforcement))
        reinforcement_dict = asdict(reinforcement)
        quantity_trace = {
            "bar_set_count": len(reinforcement.bar_sets),
            "steel_kg": ReinforcementEngine().total_steel_kg(reinforcement),
            "design_evidence_sha256": reinforcement.design_evidence_sha256,
            "status": "PRELIMINARY",
        }
        evidence = {
            "schema": "aias.design_project_evidence.v1",
            "project_id": manifest["project_id"], "scenario_id": scenario_id,
            "SYNTHETIC_TEST_DATA": True, "NOT_FOR_CONSTRUCTION": True,
            "classification": "PRELIMINARY_NOT_FOR_CONSTRUCTION",
            "reinforcement": reinforcement_dict,
            "analysis_evidence_sha256": reinforcement.analysis_evidence_sha256,
            "standards_evidence_sha256": reinforcement.standards_evidence_sha256,
            "quantity_trace": quantity_trace,
            "qa_reinforcement_trace": copy.deepcopy(quantity_trace),
        }
        filename = f"{manifest['project_id']}_DESIGN_EVIDENCE.json"
        _legacy._write(output_root / filename, evidence)
        projects.append({
            "project_id": manifest["project_id"], "scenario_id": scenario_id,
            "evidence_file": filename, "evidence_sha256": _legacy._sha256(evidence),
            "design_evidence_sha256": reinforcement.design_evidence_sha256,
            "analysis_evidence_sha256": reinforcement.analysis_evidence_sha256,
            "standards_evidence_sha256": reinforcement.standards_evidence_sha256,
            "bar_set_count": len(reinforcement.bar_sets),
            "steel_kg": quantity_trace["steel_kg"], "status": "PRELIMINARY",
            "scenario_fault": False,
            "bar_hashes_valid": all(
                item["sha256"] == _legacy._sha256({k: v for k, v in item.items() if k != "sha256"})
                for item in reinforcement_dict["bar_sets"]
            ),
            "schedule_trace_valid": all(
                item["bar_set_sha256"] in {bar["sha256"] for bar in reinforcement_dict["bar_sets"]}
                for item in reinforcement_dict["schedules"]
            ),
            "downstream_trace_valid": evidence["quantity_trace"] == evidence["qa_reinforcement_trace"],
        })

    try:
        ReinforcementEngine().build(None, {})
        missing_inputs_fail_closed = False
    except ValueError as exc:
        missing_inputs_fail_closed = "INSUFFICIENT_EVIDENCE" in str(exc)

    normal = [p for p in projects if not p["scenario_fault"]]
    faults = [p for p in projects if p["scenario_fault"]]
    checks = {
        "two_isolated_projects": len(projects) == 2 and len({p["project_id"] for p in projects}) == 2,
        "normal_design_present": len(normal) == 1,
        "stress_fault_present": len(faults) == 1 and faults[0]["scenario_id"] == "STRESS_CASE_001",
        "analysis_bound": all(len(p["analysis_evidence_sha256"]) == 64 for p in projects),
        "standards_bound": all(len(p["standards_evidence_sha256"]) == 64 for p in projects),
        "bar_sets_materialized_for_success_only": len(normal) == 1 and normal[0]["bar_set_count"] > 0 and faults[0]["bar_set_count"] == 0,
        "bar_hashes_valid": len(normal) == 1 and all(p["bar_hashes_valid"] for p in normal),
        "schedule_trace_valid": len(normal) == 1 and all(p["schedule_trace_valid"] for p in normal),
        "quantities_and_qa_bound": len(normal) == 1 and all(p["downstream_trace_valid"] for p in normal),
        "stress_emits_no_invalid_design_output": len(faults) == 1 and faults[0]["no_invalid_design_output"],
        "geometry_or_outcome_sensitive": len({p["design_evidence_sha256"] for p in projects}) == 2,
        "deterministic_reproduction": len(deterministic) == 2 and all(deterministic),
        "fail_closed_without_analysis_and_standards": missing_inputs_fail_closed,
        "scenario_faults_exactly_expected": scenario_faults == ["DESIGN-CORE-CERT-B"],
    }
    certification = {
        "schema": "aias.design_production_core_certification.v2",
        "program": "PRODUCCION DE PROYECTOS AIAS",
        "target": "DESIGN_PRODUCTION_CORE_READY",
        "prerequisite_gates": ["ANALYSIS_PRODUCTION_CORE_READY", "STANDARDS_PRODUCTION_CORE_READY"],
        "SYNTHETIC_TEST_DATA": True, "NOT_FOR_CONSTRUCTION": True,
        "classification": "PRELIMINARY_NOT_FOR_CONSTRUCTION",
        "real_project_policy": "FAIL_CLOSED_WITHOUT_AUTHENTICATED_BASELINE",
        "design_provider": "aias_reinforcement_detailing.ReinforcementEngine",
        "scenario_faults_detected": scenario_faults,
        "projects": projects, "checks": checks,
        "verdict": "DESIGN_PRODUCTION_CORE_READY" if all(checks.values()) else "NOT_READY",
    }
    _legacy._write(output_root / "DESIGN_PRODUCTION_CORE_MANIFEST.json", certification)
    return certification
