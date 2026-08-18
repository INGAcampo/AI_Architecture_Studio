from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any

from aias_building_design_core import ProjectGraph
from .project_graph_adapter import ProjectGraphStructuralAdapter


@dataclass
class AnalysisModel:
    project_id: str
    nodes: list[dict[str, Any]] = field(default_factory=list)
    members: list[dict[str, Any]] = field(default_factory=list)
    loads: list[dict[str, Any]] = field(default_factory=list)
    combinations: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema: str = "aias.analysis_model.structural.v1"


@dataclass
class StructuralResult:
    status: str
    reactions: dict[str, float]
    displacements: dict[str, float]
    drifts: dict[str, float]
    internal_forces: dict[str, float]
    code_checks: dict[str, str]
    evidence_sha256: str


class StructuralAnalysisCore:
    """Deterministic initial structural flow; not a substitute for professional sign-off."""

    def generate_model(self, graph: ProjectGraph) -> AnalysisModel:
        nodes, members, metadata = ProjectGraphStructuralAdapter().project(graph)
        return AnalysisModel(project_id=graph.project_id, nodes=nodes, members=members, metadata=metadata)

    def add_load_case(self, model: AnalysisModel, case: str, magnitude: float, direction: str = "Z") -> None:
        if magnitude < 0: raise ValueError("load magnitude must be non-negative")
        model.loads.append({"case": case, "magnitude": magnitude, "direction": direction})

    def apply_ve_combinations(self, model: AnalysisModel) -> None:
        model.combinations = [{"id": "VE-ULS-1", "factors": {"dead": 1.2, "live": 1.6}}, {"id": "VE-SLS-1", "factors": {"dead": 1.0, "live": 1.0}}]

    def solve_linear(self, model: AnalysisModel, standards_evidence: dict[str, Any] | None = None) -> StructuralResult:
        if not model.members or not model.loads or not model.combinations or standards_evidence is None:
            return self._empty("INSUFFICIENT_EVIDENCE")
        total = sum(float(load["magnitude"]) for load in model.loads)
        reactions = {node["id"]: total / max(1, sum(n["support"] for n in model.nodes)) for node in model.nodes if node["support"]}
        disp = total / 100000.0
        displacements = {node["id"]: disp for node in model.nodes}
        drifts = {node["id"]: disp / 3.0 for node in model.nodes}
        forces = {member["id"]: total / max(1, len(model.members)) for member in model.members}
        checks = {member_id: "PASS" if force < 1000 else "FAIL" for member_id, force in forces.items()}
        payload = {"reactions": reactions, "displacements": displacements, "drifts": drifts, "forces": forces, "checks": checks}
        evidence = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return StructuralResult("PASS" if all(value == "PASS" for value in checks.values()) else "FAIL", reactions, displacements, drifts, forces, checks, evidence)

    @staticmethod
    def _empty(status: str) -> StructuralResult:
        return StructuralResult(status, {}, {}, {}, {}, {}, hashlib.sha256(status.encode()).hexdigest())
