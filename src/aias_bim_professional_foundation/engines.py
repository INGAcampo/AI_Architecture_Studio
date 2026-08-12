"""Public module supporting professional BIM foundation modeling and exchange."""
from dataclasses import dataclass
from .core import Point2D

@dataclass(frozen=True, slots=True)
class WallQuantity:
    """Execute the public WallQuantity operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    gross_area_m2: float
    opening_area_m2: float
    net_area_m2: float
    net_volume_m3: float
    mass_kg: float

class QuantityEngine:
    """Execute the public QuantityEngine operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def wall(self, project, wall_id):
        """Execute the public QuantityEngine.wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        wall=project.walls[wall_id]
        opening_area=sum(o.area_m2 for o in project.openings_for(wall_id))
        net=wall.gross_area_m2-opening_area
        if net<0: raise ValueError("Negative net area.")
        volume=net*wall.thickness_m
        density=project.materials[wall.material_id].density_kg_m3
        return WallQuantity(wall.gross_area_m2,opening_area,net,volume,volume*density)

@dataclass(frozen=True, slots=True)
class AnalyticalWall:
    """Execute the public AnalyticalWall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    source_wall_id: str
    length_m: float
    area_m2: float
    material_id: str

class AnalyticalEngine:
    """Execute the public AnalyticalEngine operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def wall(self, wall):
        """Execute the public AnalyticalEngine.wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        return AnalyticalWall(wall.wall_id,wall.length_m,wall.height_m*wall.thickness_m,wall.material_id)

class JoinEngine:
    """Execute the public JoinEngine operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def classify(self,a,b,tolerance=1e-9):
        """Execute the public JoinEngine.classify operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        for p in (a.start,a.end):
            for q in (b.start,b.end):
                if p.distance_to(q)<=tolerance: return "endpoint_join"
        return "disconnected"

class SnapEngine:
    """Execute the public SnapEngine operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def wall(self,w):
        """Execute the public SnapEngine.wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        return (
            (w.start.x,w.start.y,"endpoint"),
            (w.end.x,w.end.y,"endpoint"),
            ((w.start.x+w.end.x)/2,(w.start.y+w.end.y)/2,"midpoint"),
        )
