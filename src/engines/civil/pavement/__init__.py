from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PavementLayer:
    layer_id: str
    thickness_m: float
    resilient_modulus_mpa: float
    structural_coefficient: float

    def __post_init__(self):
        if not self.layer_id.strip() or min(
            self.thickness_m,
            self.resilient_modulus_mpa,
            self.structural_coefficient,
        ) <= 0:
            raise ValueError("Capa inválida")

@dataclass(frozen=True, slots=True)
class PavementSection:
    section_id: str
    layers: tuple[PavementLayer, ...]

class PavementDesignEngine:
    def structural_number(self, section):
        return sum(
            layer.structural_coefficient * layer.thickness_m * 39.3701
            for layer in section.layers
        )

    def total_thickness(self, section):
        return sum(layer.thickness_m for layer in section.layers)
