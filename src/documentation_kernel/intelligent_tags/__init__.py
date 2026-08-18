from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TagTemplate:
    template_id: str
    pattern: str

@dataclass(frozen=True, slots=True)
class TagResult:
    element_id: str
    text: str
    missing_fields: tuple[str, ...]

class IntelligentTagEngine:
    def render(self, element_id, properties, template):
        missing = []
        text = template.pattern
        import re
        for field in re.findall(r"\{([^{}]+)\}", template.pattern):
            if field not in properties:
                missing.append(field)
                text = text.replace("{" + field + "}", "?")
            else:
                text = text.replace("{" + field + "}", str(properties[field]))
        return TagResult(element_id, text, tuple(missing))

    def batch_render(self, elements, template):
        return tuple(self.render(eid, props, template) for eid, props in elements)
