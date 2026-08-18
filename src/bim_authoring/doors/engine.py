from .geometry import DoorGeometryBuilder
from .hosting import DoorHostAdapter
from .quantities import DoorQuantityEngine
from .regeneration import DoorRegenerationEngine
from .validation import DoorValidator

class NativeBimDoorEngine:
    def __init__(self, wall_engine=None):
        self.families = {}
        self.doors = {}
        self.wall_engine = wall_engine
        self.geometry_builder = DoorGeometryBuilder()
        self.quantity_engine = DoorQuantityEngine()
        self.validator = DoorValidator()
        self.host_adapter = DoorHostAdapter()
        self.regenerator = DoorRegenerationEngine(
            self.geometry_builder,
            self.quantity_engine,
            self.validator,
        )

    def register_family(self, family):
        self.families[family.family_id] = family
        return family

    def add_door(self, door, *, auto_host=True):
        if door.family_id not in self.families:
            raise KeyError(door.family_id)
        self.doors[door.door_id] = door
        if auto_host and self.wall_engine is not None:
            from bim_authoring.walls import WallOpening
            self.host_adapter.host(door, self.wall_engine, WallOpening)
        return door

    def update_door(self, door):
        if door.door_id not in self.doors:
            raise KeyError(door.door_id)
        self.doors[door.door_id] = door
        return self.regenerate(door.door_id)

    def regenerate(self, door_id):
        door = self.doors[door_id]
        wall = None
        if self.wall_engine is not None:
            wall = self.wall_engine.walls.get(door.host_wall_id)
        return self.regenerator.regenerate(door, wall)

    def quantities(self, door_id):
        return self.quantity_engine.calculate(self.doors[door_id])
