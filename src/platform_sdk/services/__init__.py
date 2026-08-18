from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ServiceDescriptor:
    service_id:str; version:str; instance:object
class ServiceRegistry:
    def __init__(self): self._items={}
    def register(self,service_id,instance,version="1.0",replace=False):
        if service_id in self._items and not replace: raise ValueError("Servicio duplicado")
        d=ServiceDescriptor(service_id,version,instance); self._items[service_id]=d; return d
    def resolve(self,service_id): return self._items[service_id].instance
    def contains(self,service_id): return service_id in self._items
    def ids(self): return tuple(sorted(self._items))
