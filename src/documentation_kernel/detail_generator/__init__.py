from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DetailRule:
    rule_id: str
    element_kind: str
    detail_template: str

@dataclass(frozen=True, slots=True)
class DetailView:
    detail_id: str
    element_id: str
    template: str
    scale: float
    notes: tuple[str, ...]

class DetailGenerator:
    def generate(self, detail_id, element, rules, *, scale=10):
        kind = element.get("kind")
        for rule in rules:
            if rule.element_kind == kind:
                notes = tuple(element.get("notes", ()))
                return DetailView(detail_id, element["element_id"], rule.detail_template, scale, notes)
        raise ValueError(f"No existe regla de detalle para {kind}")
