"""Dependency-gated AI Office activation and intelligence-case intake."""
from __future__ import annotations
import json
from pathlib import Path
from .models import OfficeCharter,WorkItem
from .registry import OfficeRegistry
def activate_ai_office(registry:OfficeRegistry,charter_path:Path,operational_concepts:set[str])->dict:
    """Activate AI Office only when the Engineering Intelligence Core is operational."""
    row=json.loads(charter_path.read_text(encoding="utf-8"));charter=OfficeCharter(**{k:tuple(v) if isinstance(v,list) else v for k,v in row.items()});readiness=registry.dependency_readiness(charter,operational_concepts)
    if not readiness["ready"]:raise ValueError("ai_office_dependency_not_ready:"+",".join(readiness["missing"]))
    registry.register(charter);return {"activated":True,"office_id":charter.office_id,"dependencies":list(charter.dependencies)}
def route_intelligence_case(registry:OfficeRegistry,case_id:str,evidence:dict)->dict:
    """Route one intelligence-governance case to the activated AI Office."""
    return registry.route(WorkItem(case_id,"ai_governance","Review engineering intelligence recommendation","INTELLIGENCE-CORE-001",evidence))
