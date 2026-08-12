"""Public module supporting the fourth Omega integrated product release."""
from __future__ import annotations
from dataclasses import dataclass
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.graph import Relationship
from aias_omega_core.project import EngineeringProject

@dataclass(frozen=True, slots=True)
class LevelSpec:
    """Execute the public LevelSpec operation for the fourth Omega integrated product release using explicit caller inputs."""
    name: str
    elevation_m: float

class BimFactory:
    """Execute the public BimFactory operation for the fourth Omega integrated product release using explicit caller inputs."""
    def create_level(self, project: EngineeringProject, spec: LevelSpec):
        """Build the level required by the fourth Omega integrated product release from explicit inputs."""
        obj=EngineeringObject(object_type="bim_level",name=spec.name,
                              properties={"elevation_m":spec.elevation_m},classification="BIM.Level")
        return project.add_object(obj)

    def create_wall(self, project, start, end, height_m, thickness_m, material_id, level_id, name="Wall"):
        """Build the wall required by the fourth Omega integrated product release from explicit inputs."""
        dx=end[0]-start[0]; dy=end[1]-start[1]; length=(dx*dx+dy*dy)**0.5
        if min(length,height_m,thickness_m)<=0: raise ValueError("Invalid wall dimensions.")
        obj=EngineeringObject(object_type="bim_wall",name=name,
            geometry={"type":"wall","start":list(start),"end":list(end)},
            properties={"length_m":length,"height_m":height_m,"thickness_m":thickness_m,"level_id":str(level_id)},
            material_id=material_id,classification="BIM.Wall")
        oid=project.add_object(obj); project.graph.add(Relationship(level_id,oid,"hosts")); return oid

    def create_slab(self, project, points, thickness_m, material_id, level_id, name="Slab"):
        """Build the slab required by the fourth Omega integrated product release from explicit inputs."""
        if len(points)<3 or thickness_m<=0: raise ValueError("Invalid slab.")
        area=0.0
        for a,b in zip(points,points[1:]+points[:1]): area += a[0]*b[1]-b[0]*a[1]
        area=abs(area)/2.0
        obj=EngineeringObject(object_type="bim_slab",name=name,
            geometry={"type":"polygon","points":[list(p) for p in points]},
            properties={"area_m2":area,"thickness_m":thickness_m,"volume_m3":area*thickness_m,"level_id":str(level_id)},
            material_id=material_id,classification="BIM.Slab")
        oid=project.add_object(obj); project.graph.add(Relationship(level_id,oid,"hosts")); return oid

    def create_opening(self, project, wall_id, width_m, height_m, sill_m=0.0, kind="door", name="Opening"):
        """Build the opening required by the fourth Omega integrated product release from explicit inputs."""
        wall=project.objects[wall_id]
        if wall.object_type!="bim_wall": raise TypeError("Expected wall.")
        if width_m<=0 or height_m<=0: raise ValueError("Invalid opening.")
        obj=EngineeringObject(object_type=f"bim_{kind}",name=name,
            properties={"width_m":width_m,"height_m":height_m,"sill_m":sill_m,"host_wall_id":str(wall_id)},
            classification=f"BIM.{kind.title()}")
        oid=project.add_object(obj); project.graph.add(Relationship(wall_id,oid,"hosts_opening")); return oid
