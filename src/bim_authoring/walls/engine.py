from .geometry import WallGeometryBuilder
from .joins import WallJoinManager
from .openings import WallOpeningManager
from .quantities import WallQuantityEngine
from .regeneration import WallRegenerationEngine
from .validation import WallValidator

class NativeBimWallEngine:
    def __init__(self):
        self.wall_types = {}
        self.walls = {}
        self.openings = WallOpeningManager()
        self.joins = WallJoinManager()
        self.geometry_builder = WallGeometryBuilder()
        self.quantity_engine = WallQuantityEngine()
        self.validator = WallValidator()
        self.regenerator = WallRegenerationEngine(
            self.geometry_builder,
            self.quantity_engine,
            self.validator,
        )

    def register_type(self, wall_type):
        self.wall_types[wall_type.type_id] = wall_type
        return wall_type

    def add_wall(self, wall):
        if wall.wall_type.type_id not in self.wall_types:
            self.register_type(wall.wall_type)
        self.walls[wall.wall_id] = wall
        return wall

    def update_wall(self, wall):
        if wall.wall_id not in self.walls:
            raise KeyError(wall.wall_id)
        self.walls[wall.wall_id] = wall
        return self.regenerate(wall.wall_id)

    def add_opening(self, opening):
        wall = self.walls[opening.wall_id]
        return self.openings.add(wall, opening)

    def regenerate(self, wall_id):
        wall = self.walls[wall_id]
        openings = self.openings.for_wall(wall_id)
        return self.regenerator.regenerate(wall, openings)

    def quantities(self, wall_id):
        wall = self.walls[wall_id]
        return self.quantity_engine.calculate(wall, self.openings.for_wall(wall_id))
