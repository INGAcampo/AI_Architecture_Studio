from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol
@dataclass(frozen=True, slots=True)
class StructuralModel:
    model_id: str
    members: tuple[str, ...] = ()
    materials: dict[str, Any] = field(default_factory=dict)
@dataclass(frozen=True, slots=True)
class AnalysisModel:
    model_id: str
    load_cases: tuple[str, ...] = ()
    solver: str = "native-contract"
class SolverAdapter(Protocol):
    name: str
    def analyze(self, model: AnalysisModel) -> dict[str, Any]: ...
class DesignEngine:
    """Layer boundary; equations and jurisdictional rules are explicit inputs."""
    def prepare(self, structural: StructuralModel, analysis: AnalysisModel) -> dict[str, Any]:
        if not structural.model_id.strip() or not analysis.model_id.strip(): raise ValueError("model_id cannot be empty")
        if structural.model_id != analysis.model_id: raise ValueError("model_identity_mismatch")
        return {"prepared": True, "model_id": structural.model_id, "member_count": len(structural.members), "load_case_count": len(analysis.load_cases), "normative_status": "external_authority_pending"}
