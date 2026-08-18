from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SoilSpring:
    spring_id: str
    stiffness: float
    tributary_area: float
    def __post_init__(self):
        if not self.spring_id.strip() or self.stiffness <= 0 or self.tributary_area <= 0:
            raise ValueError("Datos inválidos")

class SoilInteractionEngine:
    def reaction(self, spring, settlement):
        return spring.stiffness * spring.tributary_area * settlement
