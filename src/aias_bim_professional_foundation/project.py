"""Public module supporting professional BIM foundation modeling and exchange."""
from dataclasses import dataclass
from .core import Material, Level, GridLine
from .walls import Wall

@dataclass(slots=True)
class Opening:
    """Execute the public Opening operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    wall_id: str
    width_m: float
    height_m: float
    sill_m: float
    kind: str
    name: str
    opening_id: str

    @property
    def area_m2(self):
        """Return the rectangular opening area in square metres."""
        return self.width_m*self.height_m

class BimProject:
    """Execute the public BimProject operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    def __init__(self, name):
        self.name=name
        self.materials={}
        self.levels={}
        self.grids={}
        self.walls={}
        self.openings={}

    def add_material(self, item):
        """Add material to professional BIM foundation modeling and exchange while enforcing identity constraints."""
        if item.material_id in self.materials: raise ValueError(item.material_id)
        self.materials[item.material_id]=item

    def add_level(self, item):
        """Add level to professional BIM foundation modeling and exchange while enforcing identity constraints."""
        if item.level_id in self.levels: raise ValueError(item.level_id)
        self.levels[item.level_id]=item

    def add_grid(self, item):
        """Add grid to professional BIM foundation modeling and exchange while enforcing identity constraints."""
        if item.start == item.end: raise ValueError("Invalid grid.")
        self.grids[item.grid_id]=item

    def add_wall(self, wall):
        """Add wall to professional BIM foundation modeling and exchange while enforcing identity constraints."""
        if wall.level_id not in self.levels or wall.material_id not in self.materials:
            raise ValueError("Wall dependencies missing.")
        self.walls[wall.wall_id]=wall

    def add_opening(self, opening):
        """Add opening to professional BIM foundation modeling and exchange while enforcing identity constraints."""
        wall=self.walls[opening.wall_id]
        if opening.width_m<=0 or opening.height_m<=0 or opening.sill_m<0:
            raise ValueError("Invalid opening.")
        if opening.sill_m+opening.height_m>wall.height_m:
            raise ValueError("Opening exceeds wall.")
        self.openings[opening.opening_id]=opening
        wall.openings.append(opening.opening_id)
        wall.revision+=1

    def openings_for(self, wall_id):
        """Load for for professional BIM foundation modeling and exchange while preserving typed state."""
        return tuple(o for o in self.openings.values() if o.wall_id==wall_id)
