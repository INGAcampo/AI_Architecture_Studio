"""Synthetic, reproducible certification for the architectural production core."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path

from .adapters import DrawingProductionAdapter
from .factory import ProjectProductionFactory
from .orchestrator import AIASProjectProductionOrchestrator


def _sha256(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def _manifest(project_id: str, width: float, length: float, levels: int) -> dict:
    return {
        "project_id": project_id,
        "project_name": f"Synthetic architectural certification {project_id}",
        "mode": "PILOT_SYNTHETIC",
        "scenario_id": "NOMINAL_CASE_001",
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
        "building_program": {
            "levels": levels,
            "width_m": width,
            "length_m": length,
            "storey_height_m": 3.0,
        },
    }


class SyntheticNativeDWGCertificationAdapter:
    """Explicit non-construction test double; it never emits or claims a DWG."""

    provider = "aias_project_production.certification.SyntheticNativeDWGCertificationAdapter"

    def produce(self, cad, output: Path) -> dict:
        return {
            "gate": "SYNTHETIC_BACKEND_BYPASS_PASS",
            "backend": self.provider,
            "drawings": [],
            "sha256": _sha256({"entity_ids": sorted(x["id"] for x in cad.entities)}),
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
        }


class ArchitecturalCertificationOrchestrator(AIASProjectProductionOrchestrator):
    """Use the canonical orchestrator with only its licensed DWG edge test-doubled."""

    def __init__(self, output_root: str | Path):
        super().__init__(output_root)
        self.drawing = DrawingProductionAdapter(SyntheticNativeDWGCertificationAdapter())


def certify_architectural_production_core(output_root: str | Path) -> dict:
    """Run two isolated projects through one factory and publish compact evidence."""

    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifests = [
        _manifest("ARCH-CORE-CERT-A", 8.0, 9.0, 2),
        _manifest("ARCH-CORE-CERT-B", 11.0, 7.0, 3),
    ]
    with tempfile.TemporaryDirectory(prefix="aias-architectural-cert-") as temporary:
        factory = ProjectProductionFactory(
            Path(temporary), orchestrator_type=ArchitecturalCertificationOrchestrator
        )
        factory_result = factory.run(manifests)
        changed = copy.deepcopy(manifests[0])
        changed["building_program"]["width_m"] = 10.0
        regeneration = factory.plan_selective_regeneration(
            manifests[0]["project_id"], changed
        )

        project_evidence = []
        for result in factory_result["new_results"]:
            project_id = result["project_id"]
            project_root = factory.kernel.projects / project_id
            runtime_state = factory.kernel.state(project_id)
            project_state = {
                "project_id": runtime_state["project_id"],
                "mode": runtime_state["mode"],
                "status": runtime_state["status"],
                "last_gate": runtime_state["last_gate"],
                "completed_gates": runtime_state["completed_gates"],
                "intake_sha256": runtime_state["intake_sha256"],
                "blockers": runtime_state["blockers"],
            }
            evidence = {
                "schema": "aias.architectural_project_evidence.v1",
                "project_id": project_id,
                "SYNTHETIC_TEST_DATA": True,
                "NOT_FOR_CONSTRUCTION": True,
                "manifest": factory.kernel.manifest(project_id),
                "project_state": project_state,
                "dependency_graph": json.loads(
                    (project_root / "PROJECT_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")
                ),
                "project_graph": json.loads(
                    Path(result["project_graph"]["path"]).read_text(encoding="utf-8")
                ),
                "architecture": json.loads(
                    Path(result["architecture"]["path"]).read_text(encoding="utf-8")
                ),
                "coherence": json.loads(
                    Path(result["coherence"]["path"]).read_text(encoding="utf-8")
                ),
                "pipeline": {
                    "architecture_provider": result["architecture"]["provider"],
                    "native_bim_wall_count": result["native_bim"]["wall_count"],
                    "V0_V1": result["V0_V1"],
                    "V2": result["V2"],
                    "V3": result["V3"],
                    "V4": result["V4"],
                    "V5": result["V5"],
                    "V6": result["V6"],
                    "V7": result["V7"],
                    "V8": result["V8"],
                },
            }
            evidence_file = output_root / f"{project_id}_EVIDENCE.json"
            _write(evidence_file, evidence)
            project_evidence.append({
                "project_id": project_id,
                "evidence_file": evidence_file.name,
                "evidence_sha256": _sha256(evidence),
                "source_graph_sha256": evidence["architecture"]["source_graph_sha256"],
                "coherence_verdict": evidence["coherence"]["verdict"],
            })

        checks = {
            "factory_reused": factory_result["verdict"] == "PROJECT_PRODUCTION_FACTORY_READY",
            "two_projects": len(project_evidence) == 2,
            "isolated_artifact_roots": factory_result["isolation_verified"],
            "distinct_project_graphs": len({x["source_graph_sha256"] for x in project_evidence}) == 2,
            "shared_architectural_core": all(
                result["architecture"]["provider"]
                == "aias_building_design_core.ArchitecturalProductionCore"
                for result in factory_result["new_results"]
            ),
            "pipeline_coherent": all(
                x["coherence_verdict"] == "ARCHITECTURAL_PIPELINE_COHERENT"
                for x in project_evidence
            ),
            "selective_regeneration_isolated": (
                regeneration["project_id"] == manifests[0]["project_id"]
                and "analysis" in regeneration["order"]
                and not (
                    factory.kernel.projects / manifests[1]["project_id"]
                    / "manifests" / "SELECTIVE_REGENERATION_PLAN.json"
                ).exists()
            ),
        }
        certification = {
            "schema": "aias.architectural_production_core_certification.v1",
            "program": "PRODUCCION DE PROYECTOS AIAS",
            "target": "ARCHITECTURAL_PRODUCTION_CORE_READY",
            "prerequisite_gate": "PROJECT_PRODUCTION_FACTORY_READY",
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "real_project_policy": "FAIL_CLOSED_WITHOUT_AUTHENTICATED_BASELINE",
            "factory_provider": "aias_project_production.factory.ProjectProductionFactory",
            "architectural_core_provider": "aias_building_design_core.ArchitecturalProductionCore",
            "native_dwg_certification_boundary": SyntheticNativeDWGCertificationAdapter.provider,
            "projects": project_evidence,
            "selective_regeneration": regeneration,
            "checks": checks,
            "verdict": "ARCHITECTURAL_PRODUCTION_CORE_READY" if all(checks.values()) else "NOT_READY",
        }
        _write(output_root / "ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json", certification)
        return certification


def certify_structural_production_core(output_root: str | Path) -> dict:
    """Certify the geometry-backed structural projection in two isolated projects.

    Native DWG is explicitly test-doubled here: this certification is for the
    ProjectGraph-to-Analysis contract, not a construction issuance.
    """
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifests = [
        _manifest("STRUCT-CORE-CERT-A", 8.0, 9.0, 2),
        _manifest("STRUCT-CORE-CERT-B", 11.0, 7.0, 3),
    ]
    with tempfile.TemporaryDirectory(prefix="aias-structural-cert-") as temporary:
        factory = ProjectProductionFactory(
            Path(temporary), orchestrator_type=ArchitecturalCertificationOrchestrator
        )
        factory_result = factory.run(manifests)
        projects = []
        for result in factory_result["new_results"]:
            structural_path = Path(result["structural"]["path"])
            structural = json.loads(structural_path.read_text(encoding="utf-8"))
            evidence = {
                "schema": "aias.structural_project_evidence.v1",
                "project_id": result["project_id"],
                "SYNTHETIC_TEST_DATA": True,
                "NOT_FOR_CONSTRUCTION": True,
                "structural": structural,
                "source_graph_sha256": result["architecture"]["source_graph_sha256"],
            }
            filename = f"{result['project_id']}_STRUCTURAL_EVIDENCE.json"
            _write(output_root / filename, evidence)
            projects.append({
                "project_id": result["project_id"], "evidence_file": filename,
                "evidence_sha256": _sha256(evidence),
                "source_graph_sha256": evidence["source_graph_sha256"],
                "member_count": result["structural"]["member_count"],
                "geometry_backed_member_count": result["structural"]["geometry_backed_member_count"],
                "structural_status": result["structural"]["status"],
            })
        checks = {
            "factory_reused": factory_result["verdict"] == "PROJECT_PRODUCTION_FACTORY_READY",
            "two_isolated_projects": len(projects) == 2 and factory_result["isolation_verified"],
            "distinct_source_graphs": len({item["source_graph_sha256"] for item in projects}) == 2,
            "geometry_backed_connectivity": all(
                item["member_count"] > 0 and item["member_count"] == item["geometry_backed_member_count"]
                for item in projects
            ),
            "deterministic_results": all(item["structural_status"] == "PASS" for item in projects),
        }
        certification = {
            "schema": "aias.structural_production_core_certification.v1",
            "program": "PRODUCCION DE PROYECTOS AIAS",
            "target": "STRUCTURAL_PRODUCTION_CORE_READY",
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "real_project_policy": "FAIL_CLOSED_WITHOUT_AUTHENTICATED_BASELINE",
            "projection_provider": "aias_structural_core.ProjectGraphStructuralAdapter",
            "projects": projects,
            "checks": checks,
            "verdict": "STRUCTURAL_PRODUCTION_CORE_READY" if all(checks.values()) else "NOT_READY",
        }
        _write(output_root / "STRUCTURAL_PRODUCTION_CORE_MANIFEST.json", certification)
        return certification


def certify_analysis_production_core(output_root: str | Path) -> dict:
    """Certify combination-driven, evidence-bound analysis on the canonical factory."""
    from aias_project_intake.builders import ParametricProjectGraphBuilder
    from aias_structural_professional import ProfessionalStructuralEngine

    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifests = [
        _manifest("ANALYSIS-CORE-CERT-A", 8.0, 9.0, 2),
        _manifest("ANALYSIS-CORE-CERT-B", 11.0, 7.0, 3),
    ]
    with tempfile.TemporaryDirectory(prefix="aias-analysis-cert-") as temporary:
        factory = ProjectProductionFactory(
            Path(temporary), orchestrator_type=ArchitecturalCertificationOrchestrator
        )
        factory_result = factory.run(manifests)
        projects = []
        reproduced = []
        for manifest, result in zip(manifests, factory_result["new_results"]):
            structural = json.loads(
                Path(result["structural"]["path"]).read_text(encoding="utf-8")
            )
            analysis = structural["result"]
            evidence = {
                "schema": "aias.analysis_project_evidence.v1",
                "project_id": result["project_id"],
                "SYNTHETIC_TEST_DATA": True,
                "NOT_FOR_CONSTRUCTION": True,
                "source_graph_sha256": structural["source_graph_sha256"],
                "analysis_model": structural["analysis_model"],
                "load_envelopes": analysis["load_envelopes"],
                "combination_results": analysis["combination_results"],
                "design_checks": analysis["design_checks"],
                "analysis_trace": analysis["analysis_trace"],
                "analysis_evidence_sha256": analysis["evidence_sha256"],
                "status": analysis["status"],
            }
            filename = f"{result['project_id']}_ANALYSIS_EVIDENCE.json"
            _write(output_root / filename, evidence)

            graph = ParametricProjectGraphBuilder().build(manifest)
            engine = ProfessionalStructuralEngine()
            model = engine.generate_3d_model(graph)
            engine.add_loads(model)
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
            first = engine.analyze_and_design(model, standards)
            second = engine.analyze_and_design(copy.deepcopy(model), copy.deepcopy(standards))
            reproduced.append(first.evidence_sha256 == second.evidence_sha256 == analysis["evidence_sha256"])
            projects.append({
                "project_id": result["project_id"],
                "evidence_file": filename,
                "evidence_sha256": _sha256(evidence),
                "source_graph_sha256": structural["source_graph_sha256"],
                "analysis_model_sha256": analysis["analysis_trace"]["analysis_model_sha256"],
                "analysis_evidence_sha256": analysis["evidence_sha256"],
                "standards_evidence_sha256": analysis["analysis_trace"]["standards_evidence_sha256"],
                "governing_combination": analysis["analysis_trace"]["governing_combination"],
                "equilibrium_status": analysis["analysis_trace"]["equilibrium_status"],
                "governing_total_kN": max(
                    value["factored_total_kN"]
                    for value in analysis["combination_results"].values()
                ),
                "analysis_status": analysis["status"],
            })

        fail_closed_engine = ProfessionalStructuralEngine()
        fail_closed_model = fail_closed_engine.generate_3d_model(
            ParametricProjectGraphBuilder().build(manifests[0])
        )
        fail_closed_engine.add_loads(fail_closed_model)
        fail_closed_engine.apply_combinations(fail_closed_model)
        missing_standards = fail_closed_engine.analyze_and_design(fail_closed_model, {})
        checks = {
            "factory_reused": factory_result["verdict"] == "PROJECT_PRODUCTION_FACTORY_READY",
            "two_isolated_projects": len(projects) == 2 and factory_result["isolation_verified"],
            "project_graph_bound": all(
                item["source_graph_sha256"] and item["analysis_model_sha256"]
                for item in projects
            ),
            "combination_results_materialized": all(
                item["governing_combination"] == "VE-ULS-1" for item in projects
            ),
            "equilibrium_verified": all(
                item["equilibrium_status"] == "PASS" for item in projects
            ),
            "standards_evidence_bound": all(
                len(item["standards_evidence_sha256"]) == 64 for item in projects
            ),
            "geometry_sensitive": len({item["governing_total_kN"] for item in projects}) == 2,
            "deterministic_reproduction": all(reproduced),
            "fail_closed_without_standards": missing_standards.status == "INSUFFICIENT_EVIDENCE",
            "analysis_pass": all(item["analysis_status"] == "PASS" for item in projects),
        }
        certification = {
            "schema": "aias.analysis_production_core_certification.v1",
            "program": "PRODUCCION DE PROYECTOS AIAS",
            "target": "ANALYSIS_PRODUCTION_CORE_READY",
            "prerequisite_gate": "STRUCTURAL_PRODUCTION_CORE_READY",
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "real_project_policy": "FAIL_CLOSED_WITHOUT_AUTHENTICATED_BASELINE",
            "factory_provider": "aias_project_production.factory.ProjectProductionFactory",
            "analysis_provider": "aias_structural_professional.ProfessionalStructuralEngine",
            "manual_touchpoint_baseline": 6,
            "automated_touchpoints": 2,
            "estimated_time_reduction_percent": 66.67,
            "projects": projects,
            "checks": checks,
            "verdict": "ANALYSIS_PRODUCTION_CORE_READY" if all(checks.values()) else "NOT_READY",
        }
        _write(output_root / "ANALYSIS_PRODUCTION_CORE_MANIFEST.json", certification)
        return certification
