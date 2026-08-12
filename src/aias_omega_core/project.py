"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from .events import EventBus, Event
from .graph import ObjectGraph, Relationship
from .ids import ObjectId
from .materials import MaterialLibrary
from .objects import EngineeringObject
from .selection import SelectionService
from .transactions import Transaction, TransactionManager
from .units import UnitSystem

@dataclass(slots=True)
class EngineeringProject:
    """Execute the public EngineeringProject operation for the Omega application core and shared runtime services using explicit caller inputs."""
    name: str
    path: Path | None = None
    objects: dict[ObjectId, EngineeringObject] = field(default_factory=dict)
    graph: ObjectGraph = field(default_factory=ObjectGraph)
    events: EventBus = field(default_factory=EventBus)
    transactions: TransactionManager = field(default_factory=TransactionManager)
    selection: SelectionService = field(default_factory=SelectionService)
    units: UnitSystem = field(default_factory=UnitSystem)
    materials: MaterialLibrary = field(default_factory=MaterialLibrary)
    revision: int = 0

    def add_object(self, obj: EngineeringObject) -> ObjectId:
        """Add object to the Omega application core and shared runtime services while enforcing identity constraints."""
        if obj.object_id in self.objects:
            raise ValueError("Duplicate object id.")
        self.objects[obj.object_id] = obj
        self.revision += 1

        tx = Transaction(
            name=f"Add {obj.object_type}",
            undo_steps=[lambda oid=obj.object_id: self.objects.pop(oid, None)],
            redo_steps=[lambda item=obj: self.objects.__setitem__(item.object_id, item)],
        )
        self.transactions.commit(tx)
        self.events.publish(Event("object.added", {"object_id": str(obj.object_id)}))
        return obj.object_id

    def remove_object(self, object_id: ObjectId) -> EngineeringObject:
        """Remove the requested object from the Omega application core and shared runtime services without affecting unrelated state."""
        obj = self.objects.pop(object_id)
        self.revision += 1
        tx = Transaction(
            name=f"Remove {obj.object_type}",
            undo_steps=[lambda item=obj: self.objects.__setitem__(item.object_id, item)],
            redo_steps=[lambda oid=object_id: self.objects.pop(oid, None)],
        )
        self.transactions.commit(tx)
        self.events.publish(Event("object.removed", {"object_id": str(object_id)}))
        return obj
