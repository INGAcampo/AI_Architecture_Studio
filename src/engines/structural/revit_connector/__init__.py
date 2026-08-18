from dataclasses import dataclass
import json
@dataclass(frozen=True, slots=True)
class RevitStructuralElement:
    element_id:str; category:str; type_name:str; parameters:dict
    def __post_init__(self):
        if not self.element_id.strip() or not self.category.strip(): raise ValueError("Identificadores obligatorios")
class RevitStructuralConnector:
    schema="AIAS-REVIT-STRUCT-1"
    def export_json(self, project_name, elements):
        return json.dumps({"schema":self.schema,"project_name":project_name,"elements":[{"element_id":e.element_id,"category":e.category,"type_name":e.type_name,"parameters":e.parameters} for e in elements]},sort_keys=True)
    def import_json(self,payload):
        data=json.loads(payload);return tuple(RevitStructuralElement(**item) for item in data["elements"])
