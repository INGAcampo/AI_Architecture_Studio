"""Authority registry for native AIAS domain implementations."""
from __future__ import annotations
from dataclasses import dataclass
import importlib
from typing import Any

AUTHORITY_MAP = {
    "wall": "aias_bim_professional_foundation.walls:Wall",
    "door": "bim_authoring.doors.engine:NativeBimDoorEngine",
    "window": "bim_authoring.windows.engine:NativeBimWindowEngine",
    "room": "bim_authoring.rooms_spaces:NativeBimRoomSpaceEngine",
    "properties": "aias_engineering_object.properties:PropertySystem",
    "relationships": "engines.ai.relationships.propagation:RelationshipPropagationEngine",
    "history": "cad_professional_kernel.history:HistoryManager",
    "persistence": "aias_omega_core.persistence:ProjectSerializer",
    "workspace2": "gui.bim_workspace.controller:BimWorkspaceController",
    "selection": "engines.selection.hit_test:HitTest",
}

@dataclass(frozen=True)
class AuthorityStatus:
    domain: str
    target: str
    available: bool
    error: str | None = None

class AuthorityResolver:
    """Resolve native authorities without making the canonical flow depend on signatures."""
    @staticmethod
    def resolve(target:str)->Any:
        module_name,symbol_name=target.split(":",1)
        module=importlib.import_module(module_name)
        return getattr(module,symbol_name)

    def audit(self)->list[AuthorityStatus]:
        rows=[]
        for domain,target in AUTHORITY_MAP.items():
            try:self.resolve(target);rows.append(AuthorityStatus(domain,target,True))
            except Exception as exc:rows.append(AuthorityStatus(domain,target,False,f"{type(exc).__name__}: {exc}"))
        return rows
