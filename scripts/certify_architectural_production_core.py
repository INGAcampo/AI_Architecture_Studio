"""Produce synthetic-only evidence for ARCHITECTURAL_PRODUCTION_CORE_READY."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from aias_project_production.factory import ProjectProductionFactory


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = REPO_ROOT / "engineering" / "aias" / "architectural_core_certification"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(project_id: str, width: float, length: float, levels: int) -> dict:
    return {
        "project_id": project_id,
        "project_name": f"Architectural Core Synthetic {project_id}",
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


def main() -> int:
    manifests = [
        _manifest("ARCH-CORE-CERT-A", 8.0, 9.0, 2),
        _manifest("ARCH-CORE-CERT-B", 11.0, 7.0, 3),
    ]
    factory_result = ProjectProductionFactory(OUTPUT_ROOT).run(manifests)
    if factory_result["verdict"] != "PROJECT_PRODUCTION_FACTORY_READY":
        raise RuntimeError("architectural certification factory gate failed")

    projects = []
    for source in manifests:
        project_id = source["project_id"]
        scenario_root = (
            OUTPUT_ROOT / "runtime" / "projects" / project_id / "artifacts" / source["scenario_id"]
        )
        paths = {
            "project_graph": scenario_root / "project_graph.json",
            "architecture": scenario_root / "architectural_model.json",
            "native_bim": scenario_root / "native_bim_projection.json",
            "coherence": scenario_root / "pipeline_coherence.json",
        }
        if not all(path.is_file() for path in paths.values()):
            raise RuntimeError(f"missing architectural evidence for {project_id}")
        architecture = json.loads(paths["architecture"].read_text(encoding="utf-8"))
        coherence = json.loads(paths["coherence"].read_text(encoding="utf-8"))
        if coherence.get("verdict") != "ARCHITECTURAL_PIPELINE_COHERENT":
            raise RuntimeError(f"coherence gate failed for {project_id}")
        projects.append({
            "project_id": project_id,
            "mode": source["mode"],
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "artifact_root": str(scenario_root.relative_to(REPO_ROOT)).replace("\\", "/"),
            "source_graph_sha256": architecture["source_graph_sha256"],
            "level_count": len(architecture["levels"]),
            "geometry_count": len(architecture["geometry_index"]),
            "coherence_verdict": coherence["verdict"],
            "coherence_checks": coherence["checks"],
            "artifact_sha256": {name: _sha256(path) for name, path in paths.items()},
        })

    graph_hashes = {project["source_graph_sha256"] for project in projects}
    artifact_roots = {project["artifact_root"] for project in projects}
    ready = (
        len(projects) == 2
        and len(graph_hashes) == 2
        and len(artifact_roots) == 2
        and all(all(project["coherence_checks"].values()) for project in projects)
    )
    payload = {
        "schema": "aias.architectural_production_core.certification.v1",
        "target": "ARCHITECTURAL_PRODUCTION_CORE_READY",
        "program": "PRODUCCION_DE_PROYECTOS_AIAS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "aias_building_design_core.ArchitecturalProductionCore",
        "factory": "aias_project_production.ProjectProductionFactory",
        "SYNTHETIC_TEST_DATA": True,
        "NOT_FOR_CONSTRUCTION": True,
        "real_project_policy": "AUTHENTICATED_EXTERNAL_INPUT_REQUIRED",
        "projects": projects,
        "isolation_verified": len(artifact_roots) == 2,
        "same_core_verified": True,
        "distinct_graphs_verified": len(graph_hashes) == 2,
        "tests": [
            "python -m pytest tests/project_production tests/project_intake tests/automation/test_autonomous_supervisor.py -q",
            "python -m pytest tests/project_production/test_architectural_production_core.py -q",
        ],
        "verdict": "ARCHITECTURAL_PRODUCTION_CORE_READY" if ready else "NOT_READY",
    }
    target = OUTPUT_ROOT / "ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json"
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if not ready:
        raise RuntimeError("architectural certification checks failed")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
