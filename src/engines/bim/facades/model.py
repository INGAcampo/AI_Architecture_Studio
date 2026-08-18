from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class FacadePanelKind(str, Enum):
    GLASS="glass"; OPAQUE="opaque"; SPANDREL="spandrel"; DOOR="door"; CUSTOM="custom"
class MullionOrientation(str, Enum):
    VERTICAL="vertical"; HORIZONTAL="horizontal"; DIAGONAL="diagonal"

@dataclass(frozen=True,slots=True)
class FacadeGrid:
    u_divisions:int
    v_divisions:int
    def __post_init__(self):
        if self.u_divisions<1 or self.v_divisions<1: raise ValueError("Divisiones positivas requeridas")
    @property
    def panel_count(self): return self.u_divisions*self.v_divisions

@dataclass(frozen=True,slots=True)
class FacadePanelType:
    type_id:str
    name:str
    kind:FacadePanelKind
    thickness:float
    material_id:str|None=None
    transparency:float=0.0
    metadata:dict[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not self.type_id.strip() or not self.name.strip(): raise ValueError("Identificadores obligatorios")
        if self.thickness<=0: raise ValueError("thickness positiva requerida")
        if not 0<=self.transparency<=1: raise ValueError("transparency entre 0 y 1")

@dataclass(slots=True)
class IntelligentCurtainWall:
    facade_id:str
    width:float
    height:float
    grid:FacadeGrid
    default_panel_type_id:str
    mullion_width:float=0.05
    mullion_depth:float=0.10
    panel_overrides:dict[tuple[int,int],str]=field(default_factory=dict)
    revision:int=0
    metadata:dict[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not self.facade_id.strip(): raise ValueError("facade_id obligatorio")
        if min(self.width,self.height,self.mullion_width,self.mullion_depth)<=0: raise ValueError("Dimensiones positivas requeridas")
    @property
    def panel_width(self): return self.width/self.grid.u_divisions
    @property
    def panel_height(self): return self.height/self.grid.v_divisions
    @property
    def gross_area(self): return self.width*self.height
    def touch(self): self.revision+=1; return self.revision
