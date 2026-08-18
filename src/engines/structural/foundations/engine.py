from .catalog import FoundationMaterialCatalog
from .quantities import FoundationQuantityCalculator
class IntelligentFoundationEngine:
    def __init__(self, event_dispatcher=None):
        self.materials=FoundationMaterialCatalog(); self.quantities=FoundationQuantityCalculator()
        self.event_dispatcher=event_dispatcher; self._items={}
    def register_material(self, material): self.materials.register(material); self._publish("foundation.material.registered", material_id=material.material_id)
    def add_foundation(self, foundation):
        if foundation.foundation_id in self._items: raise KeyError(foundation.foundation_id)
        self.materials.get(foundation.material_id); self._items[foundation.foundation_id]=foundation
        self._publish("foundation.added", foundation_id=foundation.foundation_id); return foundation
    def get(self, foundation_id):
        try: return self._items[foundation_id]
        except KeyError as exc: raise KeyError(f"Foundation desconocida: {foundation_id}") from exc
    def remove(self, foundation_id):
        item=self.get(foundation_id); self._items.pop(foundation_id); self._publish("foundation.removed", foundation_id=foundation_id); return item
    def resize(self, foundation_id, length, width, depth):
        if min(length,width,depth)<=0: raise ValueError("Dimensiones positivas requeridas")
        item=self.get(foundation_id); item.length=float(length); item.width=float(width); item.depth=float(depth); item.touch(); return item
    def calculate(self, foundation_id, applied_load=None):
        item=self.get(foundation_id); return self.quantities.calculate(item,self.materials.get(item.material_id),applied_load)
    def _publish(self,name,**payload):
        if callable(self.event_dispatcher): self.event_dispatcher(name,payload)
