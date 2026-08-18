from .model import IfcEntity
from .writer import IfcJsonWriter, IfcStepWriter
class NativeIfc43ExportEngine:
    def __init__(self): self._entities={}; self.json=IfcJsonWriter(); self.step=IfcStepWriter()
    def add(self, entity):
        if entity.global_id in self._entities: raise KeyError(entity.global_id)
        self._entities[entity.global_id]=entity; return entity
    def get(self,gid): return self._entities[gid]
    def all(self): return tuple(self._entities[k] for k in sorted(self._entities))
    def export_json(self): return self.json.dumps(self.all())
    def export_step(self): return self.step.dumps(self.all())
