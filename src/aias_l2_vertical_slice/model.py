"""Canonical serializable objects for the Level 2 BIM vertical slice."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
import copy
import uuid

def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"

@dataclass
class Wall:
    start: tuple[float,float]
    end: tuple[float,float]
    height: float = 3.0
    thickness: float = 0.20
    properties: dict[str,Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda:_id("WALL"))

    def length(self) -> float:
        dx=self.end[0]-self.start[0];dy=self.end[1]-self.start[1]
        return (dx*dx+dy*dy)**0.5

@dataclass
class Opening:
    kind: str
    host_wall_id: str
    offset: float
    width: float
    height: float
    sill_height: float = 0.0
    properties: dict[str,Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda:_id("OPENING"))

@dataclass
class Room:
    boundary_wall_ids: list[str]
    name: str = "Room"
    properties: dict[str,Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda:_id("ROOM"))

@dataclass
class BimProjectState:
    schema_version: str = "1.0.0"
    walls: dict[str,Wall] = field(default_factory=dict)
    openings: dict[str,Opening] = field(default_factory=dict)
    rooms: dict[str,Room] = field(default_factory=dict)
    relationships: list[dict[str,Any]] = field(default_factory=list)
    selection: list[str] = field(default_factory=list)
    revision: int = 0

    def clone(self) -> "BimProjectState":
        return copy.deepcopy(self)

    def to_dict(self) -> dict[str,Any]:
        return {
            "schema_version":self.schema_version,
            "walls":{k:asdict(v) for k,v in self.walls.items()},
            "openings":{k:asdict(v) for k,v in self.openings.items()},
            "rooms":{k:asdict(v) for k,v in self.rooms.items()},
            "relationships":copy.deepcopy(self.relationships),
            "selection":list(self.selection),
            "revision":self.revision,
        }

    @classmethod
    def from_dict(cls,data:dict[str,Any])->"BimProjectState":
        state=cls(schema_version=data.get("schema_version","1.0.0"),revision=int(data.get("revision",0)))
        state.walls={
            k:Wall(
                **{
                    **v,
                    "start":tuple(v["start"]),
                    "end":tuple(v["end"]),
                }
            )
            for k,v in data.get("walls",{}).items()
        }
        state.openings={k:Opening(**v) for k,v in data.get("openings",{}).items()}
        state.rooms={k:Room(**v) for k,v in data.get("rooms",{}).items()}
        state.relationships=list(data.get("relationships",[]))
        state.selection=list(data.get("selection",[]))
        return state
