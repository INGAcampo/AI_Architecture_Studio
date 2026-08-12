"""Public module supporting professional BIM foundation modeling and exchange."""
from dataclasses import dataclass, field
from .core import Point2D, new_id

@dataclass(slots=True)
class Wall:
    """Execute the public Wall operation for professional BIM foundation modeling and exchange using explicit caller inputs."""
    start: Point2D
    end: Point2D
    height_m: float
    thickness_m: float
    level_id: str
    material_id: str
    name: str = "Wall"
    wall_id: str = field(default_factory=new_id)
    revision: int = 0
    openings: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.start == self.end or self.height_m <= 0 or self.thickness_m <= 0:
            raise ValueError("Invalid wall geometry.")

    @property
    def length_m(self):
        """Return wall baseline length in metres."""
        return self.start.distance_to(self.end)
    @property
    def gross_area_m2(self):
        """Return gross wall elevation area before subtracting openings."""
        return self.length_m*self.height_m
    @property
    def gross_volume_m3(self):
        """Return gross wall material volume before subtracting openings."""
        return self.gross_area_m2*self.thickness_m

    def set_height(self, value):
        """Execute set height for professional BIM foundation modeling and exchange with validated state transitions."""
        if value <= 0: raise ValueError("Height must be positive.")
        if value != self.height_m:
            self.height_m=value; self.revision+=1

    def set_thickness(self, value):
        """Execute set thickness for professional BIM foundation modeling and exchange with validated state transitions."""
        if value <= 0: raise ValueError("Thickness must be positive.")
        if value != self.thickness_m:
            self.thickness_m=value; self.revision+=1
