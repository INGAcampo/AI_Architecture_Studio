"""Canonical AEOS service topology loader."""
from __future__ import annotations
import json
from pathlib import Path
from .models import ServiceDescriptor
from .registry import ServiceRegistry
def load_services(path:Path)->ServiceRegistry:
    """Load the approved service topology into a validated registry."""
    payload=json.loads(path.read_text(encoding="utf-8"));registry=ServiceRegistry()
    for row in payload["services"]:registry.register(ServiceDescriptor(**{k:tuple(v) if isinstance(v,list) else v for k,v in row.items()}))
    return registry
