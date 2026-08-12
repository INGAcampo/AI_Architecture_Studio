import json
from pathlib import Path
import pytest
from aias_engineering_agents import AgentRole, EngineeringAgentWorkflow
ROOT=Path(__file__).resolve().parents[1]
def test_agent_requires_deterministic_services_and_gates():
    flow=EngineeringAgentWorkflow({"geometry.validate","standards.check","bim.export"})
    plan=flow.plan("req-1",AgentRole.STRUCTURAL,"check beam",("geometry.validate","standards.check"),("geometry","normative"))
    assert flow.authorize_execution(plan)["authorized"] is False
def test_agent_rejects_unknown_service():
    with pytest.raises(ValueError,match="unknown_deterministic_services"): EngineeringAgentWorkflow(set()).plan("r",AgentRole.BIM,"x",("invent",),("qa",))
def test_agent_spec_prohibits_invented_results():
    spec=json.loads((ROOT/"engineering/aias/engineering_agents/AI_ENGINEERING_AGENTS_001_SPEC.json").read_text(encoding="utf-8"))
    assert "invent structural results" in spec["prohibited_responsibilities"]
