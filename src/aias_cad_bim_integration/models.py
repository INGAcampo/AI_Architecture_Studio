"""Neutral unit-explicit contracts for controlled CAD/BIM exchange."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
@dataclass(frozen=True,slots=True)
class BimElement:
    """Represent a stable BIM element and its planar geometric footprint."""
    element_id:str;element_type:str;name:str;footprint_mm:tuple[tuple[float,float],...];properties:dict=field(default_factory=dict);source_ref:str="";version:str="1.0.0"
    def validate(self):
        """Reject incomplete, degenerate or unattributed BIM elements."""
        if not self.element_id or not self.element_type or not self.name or not self.source_ref:raise ValueError("invalid_bim_element_identity")
        if len(self.footprint_mm)<3 or any(len(point)!=2 for point in self.footprint_mm):raise ValueError("invalid_bim_footprint")
@dataclass(frozen=True,slots=True)
class InterchangeModel:
    """Aggregate explicitly versioned BIM elements in canonical millimetres."""
    model_id:str;version:str;units:str;elements:tuple[BimElement,...];provenance:dict=field(default_factory=dict)
    def to_dict(self):
        """Project the interchange model into its stable dictionary representation."""
        return asdict(self)
@dataclass(frozen=True,slots=True)
class MappingResult:
    """Return generated drawing identity, element mappings and disclosed losses."""
    drawing_id:str;mappings:tuple[dict,...];losses:tuple[dict,...];synchronized_properties:dict=field(default_factory=dict)
