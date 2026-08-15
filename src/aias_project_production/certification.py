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
