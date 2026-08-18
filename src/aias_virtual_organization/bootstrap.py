"""Canonical virtual-engineer roster loader."""
from __future__ import annotations
import json
from pathlib import Path
from .models import VirtualEngineer
from .organization import VirtualEngineeringOrganization
def load_roster(organization:VirtualEngineeringOrganization,path:Path)->dict:
    """Load the approved roster while preserving non-professional legal status."""
    payload=json.loads(path.read_text(encoding="utf-8"));ids=[]
    for row in payload["engineers"]:organization.register(VirtualEngineer(**{k:tuple(v) if isinstance(v,list) else v for k,v in row.items()}));ids.append(row["engineer_id"])
    return {"registered":ids,"count":len(ids),"legal_status":payload["legal_status"]}
