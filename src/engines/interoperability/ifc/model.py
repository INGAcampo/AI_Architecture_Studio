from dataclasses import dataclass, field
from enum import Enum
from typing import Any
class IfcEntityKind(str, Enum):
    PROJECT="IfcProject"; SITE="IfcSite"; BUILDING="IfcBuilding"; STOREY="IfcBuildingStorey"
    WALL="IfcWall"; SLAB="IfcSlab"; ROOF="IfcRoof"; DOOR="IfcDoor"; WINDOW="IfcWindow"
    BEAM="IfcBeam"; COLUMN="IfcColumn"; FOOTING="IfcFooting"; STAIR="IfcStair"; CURTAIN_WALL="IfcCurtainWall"
@dataclass(frozen=True, slots=True)
class IfcEntity:
    global_id: str
    kind: IfcEntityKind
    name: str
    properties: dict[str, Any] = field(default_factory=dict)
    relationships: tuple[str, ...] = ()
    def __post_init__(self):
        if not self.global_id.strip() or not self.name.strip(): raise ValueError("Identificadores obligatorios")
