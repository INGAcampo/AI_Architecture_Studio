from dataclasses import dataclass
from cad_professional_kernel.geometry import Point2D

@dataclass(slots=True)
class DynamicInput:
    prompt: str = "Comando:"
    distance: float | None = None
    angle: float | None = None
    absolute_point: Point2D | None = None

    def clear(self) -> None:
        self.prompt = "Comando:"
        self.distance = None
        self.angle = None
        self.absolute_point = None
