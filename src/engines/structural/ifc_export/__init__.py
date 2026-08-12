from dataclasses import dataclass, field
import json

@dataclass(frozen=True, slots=True)
class IfcExportEntity:
    global_id: str
    entity_type: str
    name: str
    property_sets: dict = field(default_factory=dict)
    materials: tuple[str, ...] = ()
    parent_id: str | None = None

    def __post_init__(self):
        if not self.global_id.strip() or not self.entity_type.strip():
            raise ValueError("Identificadores IFC obligatorios")

class Ifc43ExportEngine:
    schema = "IFC4X3"

    def export_json(self, entities):
        return json.dumps({
            "schema": self.schema,
            "entities": [{
                "global_id": entity.global_id,
                "entity_type": entity.entity_type,
                "name": entity.name,
                "property_sets": entity.property_sets,
                "materials": list(entity.materials),
                "parent_id": entity.parent_id,
            } for entity in entities],
        }, sort_keys=True)

    def export_step_subset(self, entities):
        lines = [
            "ISO-10303-21;",
            "HEADER;",
            "FILE_SCHEMA(('IFC4X3'));",
            "ENDSEC;",
            "DATA;",
        ]
        for index, entity in enumerate(entities, 1):
            lines.append(
                f"#{index}={entity.entity_type.upper()}('{entity.global_id}','{entity.name}');"
            )
        lines.extend(["ENDSEC;", "END-ISO-10303-21;"])
        return "\n".join(lines)
