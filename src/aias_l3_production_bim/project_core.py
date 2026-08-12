"""Project document entities for AIAS Level 3 production BIM."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import copy, uuid

def _id(prefix:str)->str:
    """Return a compact stable project entity identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"

@dataclass(slots=True)
class ProjectInfo:
    """Describe one production BIM project document."""
    name:str
    number:str=""
    description:str=""
    units:str="metric"
    id:str=field(default_factory=lambda:_id("PRJ"))

@dataclass(slots=True)
class Level:
    """Represent a building level/storey."""
    name:str
    elevation:float
    id:str=field(default_factory=lambda:_id("LVL"))
    properties:dict[str,Any]=field(default_factory=dict)

@dataclass(slots=True)
class Grid:
    """Represent a straight project datum/grid."""
    name:str
    start:tuple[float,float]
    end:tuple[float,float]
    id:str=field(default_factory=lambda:_id("GRID"))
    properties:dict[str,Any]=field(default_factory=dict)

@dataclass(slots=True)
class ProjectView:
    """Represent a named project view."""
    name:str
    view_type:str
    level_id:str|None=None
    id:str=field(default_factory=lambda:_id("VIEW"))
    properties:dict[str,Any]=field(default_factory=dict)

@dataclass(slots=True)
class Sheet:
    """Represent one drawing sheet."""
    number:str
    name:str
    view_ids:list[str]=field(default_factory=list)
    id:str=field(default_factory=lambda:_id("SHEET"))
    properties:dict[str,Any]=field(default_factory=dict)

@dataclass(slots=True)
class ProjectDocumentState:
    """Store Level 3 project state around the certified Level 2 BIM slice."""
    project:ProjectInfo
    levels:dict[str,Level]=field(default_factory=dict)
    grids:dict[str,Grid]=field(default_factory=dict)
    views:dict[str,ProjectView]=field(default_factory=dict)
    sheets:dict[str,Sheet]=field(default_factory=dict)
    active_view_id:str|None=None
    selected_object_ids:list[str]=field(default_factory=list)
    revision:int=0
    def clone(self):
        """Return a deep copy."""
        return copy.deepcopy(self)
    def to_dict(self)->dict[str,Any]:
        """Serialize to deterministic JSON-compatible data."""
        return {
            "project":{"id":self.project.id,"name":self.project.name,"number":self.project.number,"description":self.project.description,"units":self.project.units},
            "levels":{k:{"id":v.id,"name":v.name,"elevation":v.elevation,"properties":copy.deepcopy(v.properties)} for k,v in self.levels.items()},
            "grids":{k:{"id":v.id,"name":v.name,"start":list(v.start),"end":list(v.end),"properties":copy.deepcopy(v.properties)} for k,v in self.grids.items()},
            "views":{k:{"id":v.id,"name":v.name,"view_type":v.view_type,"level_id":v.level_id,"properties":copy.deepcopy(v.properties)} for k,v in self.views.items()},
            "sheets":{k:{"id":v.id,"number":v.number,"name":v.name,"view_ids":list(v.view_ids),"properties":copy.deepcopy(v.properties)} for k,v in self.sheets.items()},
            "active_view_id":self.active_view_id,"selected_object_ids":list(self.selected_object_ids),"revision":self.revision}
    @classmethod
    def from_dict(cls,data):
        """Restore canonical project state."""
        s=cls(project=ProjectInfo(**data["project"]))
        s.levels={k:Level(**v) for k,v in data.get("levels",{}).items()}
        s.grids={k:Grid(**{**v,"start":tuple(v["start"]),"end":tuple(v["end"])}) for k,v in data.get("grids",{}).items()}
        s.views={k:ProjectView(**v) for k,v in data.get("views",{}).items()}
        s.sheets={k:Sheet(**v) for k,v in data.get("sheets",{}).items()}
        s.active_view_id=data.get("active_view_id"); s.selected_object_ids=list(data.get("selected_object_ids",[])); s.revision=int(data.get("revision",0))
        return s
