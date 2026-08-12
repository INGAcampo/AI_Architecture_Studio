from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True, slots=True)
class SpaceRequirement:
    space_id: str
    minimum_area: float
    aspect_ratio: float = 1.0

@dataclass(frozen=True, slots=True)
class LayoutSpace:
    space_id: str
    x: float
    y: float
    width: float
    height: float

    @property
    def area(self):
        return self.width * self.height

@dataclass(frozen=True, slots=True)
class LayoutSolution:
    spaces: tuple[LayoutSpace, ...]
    total_area: float
    compactness: float

class GenerativeLayoutEngine:
    def generate_linear(self, requirements, *, corridor_width=1.5):
        x = 0.0
        spaces = []
        for requirement in requirements:
            width = sqrt(requirement.minimum_area * requirement.aspect_ratio)
            height = requirement.minimum_area / width
            spaces.append(LayoutSpace(requirement.space_id, x, 0.0, width, height))
            x += width + corridor_width
        total_area = sum(space.area for space in spaces)
        envelope_width = max((space.x + space.width for space in spaces), default=0)
        envelope_height = max((space.height for space in spaces), default=0)
        compactness = total_area / (envelope_width * envelope_height) if envelope_width and envelope_height else 0
        return LayoutSolution(tuple(spaces), total_area, compactness)

    def adjacency_score(self, layout, desired_pairs):
        positions = {space.space_id: space for space in layout.spaces}
        score = 0
        for left, right in desired_pairs:
            a, b = positions[left], positions[right]
            gap = max(0.0, b.x - (a.x + a.width), a.x - (b.x + b.width))
            score += 1.0 / (1.0 + gap)
        return score
