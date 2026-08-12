from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DeformedNode:
    node_id: str
    x: float
    y: float
    z: float
    ux: float
    uy: float
    uz: float
    def __post_init__(self):
        if not self.node_id.strip():
            raise ValueError("node_id obligatorio")
    def deformed_position(self, scale=1.0):
        return (self.x + self.ux*scale, self.y + self.uy*scale, self.z + self.uz*scale)
    @property
    def displacement_magnitude(self):
        return (self.ux**2 + self.uy**2 + self.uz**2) ** 0.5

class ReactionPostprocessor:
    def resultant(self, reactions):
        return tuple(sum(values[i] for values in reactions) for i in range(3))
