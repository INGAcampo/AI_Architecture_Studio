"""Text, linear-dimension and leader annotation contracts."""
from dataclasses import dataclass
from .geometry import Point

@dataclass(slots=True)
class TextNote:
    """Positioned drawing text with height and layer."""
    text: str
    position: Point
    height: float = 2.5

@dataclass(slots=True)
class LinearDimension:
    """Measured linear annotation between extension points."""
    start: Point
    end: Point
    offset: float = 1.0

    @property
    def measured_value(self) -> float:
        """Execute the public LinearDimension.measured_value operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return self.start.distance_to(self.end)

@dataclass(slots=True)
class Leader:
    """Callout text connected to a target by a leader path."""
    start: Point
    end: Point
    text: str
