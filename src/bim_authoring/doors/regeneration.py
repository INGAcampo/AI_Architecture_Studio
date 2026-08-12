from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DoorRegenerationResult:
    door_id: str
    previous_revision: int
    new_revision: int
    geometry: object
    quantities: object
    issues: tuple

class DoorRegenerationEngine:
    def __init__(self, geometry_builder, quantity_engine, validator):
        self.geometry_builder = geometry_builder
        self.quantity_engine = quantity_engine
        self.validator = validator

    def regenerate(self, door, wall=None):
        return DoorRegenerationResult(
            door_id=door.door_id,
            previous_revision=max(0, door.revision - 1),
            new_revision=door.revision,
            geometry=self.geometry_builder.build(door),
            quantities=self.quantity_engine.calculate(door),
            issues=self.validator.validate(door, wall),
        )
