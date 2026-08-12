from dataclasses import dataclass
from enum import Enum
import json

class ConnectorTarget(str, Enum):
    SAP2000="SAP2000"
    ETABS="ETABS"

@dataclass(frozen=True, slots=True)
class ConnectorModel:
    project_name: str
    nodes: tuple[dict, ...]
    members: tuple[dict, ...]
    load_cases: tuple[dict, ...] = ()
    def __post_init__(self):
        if not self.project_name.strip():
            raise ValueError("project_name obligatorio")

class SapEtabsConnector:
    schema_version = "AIAS-STRUCT-1"
    def export_json(self, model, target):
        return json.dumps({
            "schema": self.schema_version,
            "target": target.value,
            "project_name": model.project_name,
            "nodes": list(model.nodes),
            "members": list(model.members),
            "load_cases": list(model.load_cases),
        }, sort_keys=True)
    def import_json(self, payload):
        data = json.loads(payload)
        return ConnectorModel(
            data["project_name"],
            tuple(data.get("nodes", ())),
            tuple(data.get("members", ())),
            tuple(data.get("load_cases", ())),
        )
