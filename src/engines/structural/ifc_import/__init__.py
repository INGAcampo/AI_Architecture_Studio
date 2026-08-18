from dataclasses import dataclass, field
import json

@dataclass(frozen=True, slots=True)
class ImportedIfcEntity:
    global_id: str
    entity_type: str
    name: str
    properties: dict = field(default_factory=dict)
    parent_id: str | None = None

    def __post_init__(self):
        if not self.global_id.strip() or not self.entity_type.strip():
            raise ValueError("Identificadores IFC obligatorios")

class Ifc43ImportEngine:
    supported_schema = "IFC4X3"

    def import_json(self, payload):
        data = json.loads(payload)
        if data.get("schema") != self.supported_schema:
            raise ValueError("Esquema IFC no soportado")
        return tuple(
            ImportedIfcEntity(
                item["global_id"],
                item["entity_type"],
                item.get("name", ""),
                item.get("properties", {}),
                item.get("parent_id"),
            )
            for item in data.get("entities", ())
        )

    def by_type(self, entities, entity_type):
        return tuple(entity for entity in entities if entity.entity_type == entity_type)

    def spatial_roots(self, entities):
        return tuple(entity for entity in entities if entity.parent_id is None)
