from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CrossSectionComponent:
    component_id: str
    width: float
    slope: float
    material: str

    def __post_init__(self):
        if not self.component_id.strip() or self.width <= 0 or not self.material.strip():
            raise ValueError("Componente inválido")

@dataclass(frozen=True, slots=True)
class RoadTemplate:
    template_id: str
    components: tuple[CrossSectionComponent, ...]

    def __post_init__(self):
        if not self.template_id.strip() or not self.components:
            raise ValueError("Plantilla inválida")

class CrossSectionEngine:
    def total_width(self, template):
        return sum(component.width for component in template.components)

    def material_widths(self, template):
        result = {}
        for component in template.components:
            result[component.material] = result.get(component.material, 0.0) + component.width
        return result
