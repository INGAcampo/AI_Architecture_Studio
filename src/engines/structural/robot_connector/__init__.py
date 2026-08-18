from dataclasses import dataclass
import json
@dataclass(frozen=True, slots=True)
class RobotBar:
    bar_id:str; start_node:str; end_node:str; section_name:str; material_name:str
    def __post_init__(self):
        if not self.bar_id.strip() or not self.start_node.strip() or not self.end_node.strip(): raise ValueError("Datos inválidos")
class RobotStructuralConnector:
    schema="AIAS-ROBOT-1"
    def export_json(self,bars):
        return json.dumps({"schema":self.schema,"bars":[{"bar_id":b.bar_id,"start_node":b.start_node,"end_node":b.end_node,"section_name":b.section_name,"material_name":b.material_name} for b in bars]},sort_keys=True)
    def import_json(self,payload):
        data=json.loads(payload);return tuple(RobotBar(**item) for item in data["bars"])
