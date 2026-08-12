"""Canonical dependency-ready enterprise-office charter loader."""
from __future__ import annotations
import json
from pathlib import Path
from .models import OfficeCharter
from .registry import OfficeRegistry

def load_charters(registry:OfficeRegistry,path:Path)->dict:
    """Register every approved charter and report intentionally deferred offices."""
    payload=json.loads(path.read_text(encoding="utf-8"));registered=[]
    for row in payload["offices"]:registry.register(OfficeCharter(**{key:tuple(value) if isinstance(value,list) else value for key,value in row.items()}));registered.append(row["office_id"])
    return {"registered":registered,"deferred":payload["deferred"]}
