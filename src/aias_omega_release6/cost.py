"""Public module supporting the sixth Omega integrated product release."""
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class CostItem:
    """Execute the public CostItem operation for the sixth Omega integrated product release using explicit caller inputs."""
    code:str; description:str; unit:str; unit_price:float
@dataclass(frozen=True, slots=True)
class BoqLine:
    """Execute the public BoqLine operation for the sixth Omega integrated product release using explicit caller inputs."""
    code:str; description:str; unit:str; quantity:float; unit_price:float
    @property
    def total(self):
        """Return extended line cost as quantity times unit price."""
        return self.quantity*self.unit_price
class CostCatalog:
    """Execute the public CostCatalog operation for the sixth Omega integrated product release using explicit caller inputs."""
    def __init__(self): self._items={}
    def add(self,item):
        """Add add to the sixth Omega integrated product release while enforcing identity constraints."""
        if item.code in self._items: raise ValueError(item.code)
        self._items[item.code]=item
    def get(self,code):
        """Return the uniquely registered cost item for a code."""
        return self._items[code]
class BoqEngine:
    """Execute the public BoqEngine operation for the sixth Omega integrated product release using explicit caller inputs."""
    def from_bim(self,project,catalog):
        """Execute the public BoqEngine.from_bim operation for the sixth Omega integrated product release using explicit caller inputs."""
        lines=[]
        wall_volume=sum(float(o.properties.get("volume_m3",0)) for o in project.objects.values() if o.object_type=="quantity_item")
        slab_volume=sum(float(o.properties.get("volume_m3",0)) for o in project.objects.values() if o.object_type=="bim_slab")
        if wall_volume:
            item=catalog.get("CONC-WALL"); lines.append(BoqLine(item.code,item.description,item.unit,wall_volume,item.unit_price))
        if slab_volume:
            item=catalog.get("CONC-SLAB"); lines.append(BoqLine(item.code,item.description,item.unit,slab_volume,item.unit_price))
        return tuple(lines)
