from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True, slots=True)
class StructuralSlabType:
    type_id:str
    name:str
    thickness:float
    material_id:str

@dataclass(frozen=True, slots=True)
class StructuralSlab:
    slab_id:str
    slab_type:StructuralSlabType
    boundary:tuple[tuple[float,float],...]
    openings:tuple[tuple[tuple[float,float],...],...]=()
    elevation:float=0.0
    level_id:str|None=None

@dataclass(frozen=True, slots=True)
class StructuralSlabQuantities:
    gross_area:float
    opening_area:float
    net_area:float
    volume:float
    perimeter:float

class StructuralSlabEngine:
    def _area(self,pts):
        return abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))/2
    def _perimeter(self,pts):
        return sum(hypot(pts[(i+1)%len(pts)][0]-pts[i][0],pts[(i+1)%len(pts)][1]-pts[i][1]) for i in range(len(pts)))
    def quantities(self,slab):
        gross=self._area(slab.boundary)
        openings=sum(self._area(o) for o in slab.openings)
        net=max(0.0,gross-openings)
        return StructuralSlabQuantities(gross,openings,net,net*slab.slab_type.thickness,self._perimeter(slab.boundary))
    def validate(self,slab):
        issues=[]
        if len(slab.boundary)<3: issues.append("invalid_boundary")
        if slab.slab_type.thickness<=0: issues.append("invalid_thickness")
        return tuple(issues)
