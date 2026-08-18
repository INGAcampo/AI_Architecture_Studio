from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConcreteSection:
    section_id: str
    width: float
    depth: float
    concrete_strength: float
    steel_yield_strength: float
    steel_area: float
    def __post_init__(self):
        if not self.section_id.strip() or min(self.width, self.depth, self.concrete_strength, self.steel_yield_strength, self.steel_area) <= 0:
            raise ValueError("Datos inválidos")

class ReinforcedConcreteDesignEngine:
    def nominal_moment(self, section):
        a = section.steel_area * section.steel_yield_strength / (0.85 * section.concrete_strength * section.width)
        lever_arm = section.depth - a / 2
        return section.steel_area * section.steel_yield_strength * lever_arm
    def design_strength(self, section, phi=0.9):
        return phi * self.nominal_moment(section)
    def reinforcement_ratio(self, section):
        return section.steel_area / (section.width * section.depth)
