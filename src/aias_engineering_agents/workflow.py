from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any
class AgentRole(str, Enum):
    ARCHITECT="architect"; STRUCTURAL="structural"; BIM="bim"; QA="qa"; DOCUMENT="document"
@dataclass(frozen=True, slots=True)
class AgentPlan:
    request_id: str
    role: AgentRole
    intent: str
    deterministic_services: tuple[str, ...]
    validation_gates: tuple[str, ...]
@dataclass(slots=True)
class EngineeringAgentWorkflow:
    allowed_services: set[str]
    def plan(self, request_id: str, role: AgentRole, intent: str, services: tuple[str, ...], gates: tuple[str, ...]) -> AgentPlan:
        if not request_id.strip() or not intent.strip(): raise ValueError("request_id_and_intent_required")
        unknown=set(services)-self.allowed_services
        if unknown: raise ValueError("unknown_deterministic_services:" + ",".join(sorted(unknown)))
        if not gates: raise ValueError("validation_gates_required")
        return AgentPlan(request_id,role,intent,services,gates)
    def authorize_execution(self, plan: AgentPlan, *, validated: bool = False) -> dict[str, Any]:
        return {"authorized": bool(validated), "request_id": plan.request_id, "reason": "deterministic validation required before execution" if not validated else "validated service execution authorized", "ai_result_generation": False}
