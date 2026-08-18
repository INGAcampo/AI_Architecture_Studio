from .validation import CirculationValidator
from .quantities import CirculationQuantityCalculator
class IntelligentCirculationEngine:
    def __init__(self,event_dispatcher=None):
        self.validator=CirculationValidator(); self.quantities=CirculationQuantityCalculator(); self.event_dispatcher=event_dispatcher; self._items={}
    def add(self,item):
        if item.circulation_id in self._items: raise KeyError(item.circulation_id)
        result=self.validator.validate(item)
        if not result.valid: raise ValueError("; ".join(result.errors))
        self._items[item.circulation_id]=item; self._publish("circulation.added",circulation_id=item.circulation_id); return item
    def get(self,item_id):
        try:return self._items[item_id]
        except KeyError as exc: raise KeyError(f"Circulación desconocida: {item_id}") from exc
    def remove(self,item_id):
        item=self.get(item_id); self._items.pop(item_id); return item
    def resize(self,item_id,width=None,riser_height=None,tread_depth=None):
        item=self.get(item_id)
        if width is not None:item.width=float(width)
        if riser_height is not None:item.riser_height=float(riser_height)
        if tread_depth is not None:item.tread_depth=float(tread_depth)
        result=self.validator.validate(item)
        if not result.valid: raise ValueError("; ".join(result.errors))
        item.touch(); return item
    def calculate(self,item_id): return self.quantities.calculate(self.get(item_id))
    def _publish(self,name,**payload):
        if callable(self.event_dispatcher): self.event_dispatcher(name,payload)
