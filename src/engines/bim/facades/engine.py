from .catalog import FacadePanelCatalog
from .quantities import FacadeQuantityCalculator
class IntelligentFacadeEngine:
    def __init__(self,event_dispatcher=None):
        self.catalog=FacadePanelCatalog();self.quantities=FacadeQuantityCalculator();self.event_dispatcher=event_dispatcher;self._items={}
    def register_panel_type(self,item):self.catalog.register(item);self._publish("facade.panel_type.registered",type_id=item.type_id)
    def add(self,facade):
        if facade.facade_id in self._items:raise KeyError(facade.facade_id)
        self.catalog.get(facade.default_panel_type_id);self._items[facade.facade_id]=facade;self._publish("facade.added",facade_id=facade.facade_id);return facade
    def get(self,facade_id):
        try:return self._items[facade_id]
        except KeyError as exc:raise KeyError(f"Facade desconocida: {facade_id}") from exc
    def override_panel(self,facade_id,u,v,type_id):
        self.catalog.get(type_id);f=self.get(facade_id)
        if not 0<=u<f.grid.u_divisions or not 0<=v<f.grid.v_divisions:raise IndexError("Panel fuera de rango")
        f.panel_overrides[(u,v)]=type_id;f.touch();return f
    def resize(self,facade_id,width,height):
        if min(width,height)<=0:raise ValueError("Dimensiones positivas requeridas")
        f=self.get(facade_id);f.width=float(width);f.height=float(height);f.touch();return f
    def calculate(self,facade_id):return self.quantities.calculate(self.get(facade_id),self.catalog)
    def _publish(self,name,**payload):
        if callable(self.event_dispatcher):self.event_dispatcher(name,payload)
