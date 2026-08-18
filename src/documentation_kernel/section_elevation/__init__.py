from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ModelElement:
    element_id: str
    x: float
    y: float
    z: float
    width: float
    height: float

@dataclass(frozen=True, slots=True)
class GeneratedView:
    view_id: str
    kind: str
    visible_element_ids: tuple[str, ...]
    bounds: tuple[float, float, float, float]

class SectionElevationGenerator:
    def section(self, view_id, elements, cut_x, depth):
        visible = tuple(
            e.element_id for e in elements
            if cut_x <= e.x <= cut_x + depth
        )
        return GeneratedView(view_id, "section", visible, (cut_x, 0, cut_x + depth, 0))

    def elevation(self, view_id, elements, direction="north"):
        ids = tuple(sorted(e.element_id for e in elements))
        max_x = max((e.x + e.width for e in elements), default=0)
        max_z = max((e.z + e.height for e in elements), default=0)
        return GeneratedView(view_id, f"elevation-{direction}", ids, (0, 0, max_x, max_z))
