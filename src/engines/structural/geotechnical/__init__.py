from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SoilLayer:
    layer_id: str
    thickness: float
    unit_weight: float
    cohesion: float
    friction_angle_deg: float
    def __post_init__(self):
        if not self.layer_id.strip() or self.thickness <= 0 or self.unit_weight <= 0:
            raise ValueError("Datos inválidos")

class GeotechnicalModel:
    def vertical_stress(self, layers):
        return sum(layer.thickness * layer.unit_weight for layer in layers)
