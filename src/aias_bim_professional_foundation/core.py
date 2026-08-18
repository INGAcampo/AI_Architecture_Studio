"""Public module supporting professional BIM foundation modeling and exchange."""
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass(frozen=True, slots=True)
class Point2D:
    """Execute the public Point2D operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    x: float
    y: float
    def distance_to(self, other):
        """Execute the public Point2D.distance_to operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
        return ((other.x-self.x)**2+(other.y-self.y)**2)**0.5

@dataclass(frozen=True, slots=True)
class Material:
    """Execute the public Material operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    material_id: str
    name: str
    category: str
    density_kg_m3: float
    properties: dict = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class Level:
    """Execute the public Level operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    level_id: str
    name: str
    elevation_m: float

@dataclass(frozen=True, slots=True)
class GridLine:
    """Execute the public GridLine operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    grid_id: str
    name: str
    start: Point2D
    end: Point2D

def new_id():
    """Build the id required by professional BIM foundation modeling and exchange from explicit inputs."""
    return uuid4().hex
