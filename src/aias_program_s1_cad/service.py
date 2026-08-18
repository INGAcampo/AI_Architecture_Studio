"""Application service coordinating CAD document state and command subsystems."""
from .layers import LayerEngine
from .selection import SelectionEngine
from .snaps import SnapEngine
from .editing import EditingEngine
from .blocks import BlockEngine

class CadFoundationService:
    """Expose the integrated layer, selection, snap, edit, block and command engines."""
    def __init__(self) -> None:
        self.entities=[]
        self.layers=LayerEngine()
        self.selection=SelectionEngine()
        self.snaps=SnapEngine()
        self.editing=EditingEngine()
        self.blocks=BlockEngine()

    def add(self, entity):
        """Add add to the S1 professional CAD foundation program while enforcing identity constraints."""
        if entity.layer not in {layer.name for layer in self.layers.all()}:
            raise ValueError(f"Unknown layer: {entity.layer}")
        self.entities.append(entity)
        return entity.entity_id

    def remove(self, entity_id):
        """Remove the requested remove from the S1 professional CAD foundation program without affecting unrelated state."""
        for i,e in enumerate(self.entities):
            if e.entity_id==entity_id:
                return self.entities.pop(i)
        raise KeyError(entity_id)
