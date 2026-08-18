from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WallRegenerationResult:
    wall_id: str
    previous_revision: int
    new_revision: int
    geometry: object
    quantities: object
    issues: tuple

class WallRegenerationEngine:
    def __init__(self, geometry_builder, quantity_engine, validator):
        self.geometry_builder = geometry_builder
        self.quantity_engine = quantity_engine
        self.validator = validator

    def regenerate(self, wall, openings=()):
        geometry = self.geometry_builder.build(wall)
        quantities = self.quantity_engine.calculate(wall, openings)
        issues = self.validator.validate(wall, openings)
        return WallRegenerationResult(
            wall_id=wall.wall_id,
            previous_revision=max(0, wall.revision - 1),
            new_revision=wall.revision,
            geometry=geometry,
            quantities=quantities,
            issues=issues,
        )
