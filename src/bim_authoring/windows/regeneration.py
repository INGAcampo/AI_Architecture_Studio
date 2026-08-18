from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WindowRegenerationResult:
    window_id: str
    previous_revision: int
    new_revision: int
    geometry: object
    quantities: object
    issues: tuple

class WindowRegenerationEngine:
    def __init__(self, geometry_builder, quantity_engine, validator):
        self.geometry_builder = geometry_builder
        self.quantity_engine = quantity_engine
        self.validator = validator

    def regenerate(self, window, wall=None):
        return WindowRegenerationResult(
            window_id=window.window_id,
            previous_revision=max(0, window.revision - 1),
            new_revision=window.revision,
            geometry=self.geometry_builder.build(window),
            quantities=self.quantity_engine.calculate(window),
            issues=self.validator.validate(window, wall),
        )
