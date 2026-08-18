"""AIAS BIM Engine — arquitectura, adaptadores y servicio central."""

from .adapters import (
    BimAdapter,
    BimAdapterRegistry,
    create_default_bim_adapter_registry,
)
from .categories import BimCategory
from .document import BimDocument
from .element import BimElement
from .parameters import BimParameterSet
from .relationships import BimRelationship, RelationshipType
from .schema import BIM_SCHEMA_VERSION
from .services import (
    BimDocumentRepository,
    BimEvent,
    BimEventDispatcher,
    BimEventName,
    BimParameterManager,
    BimRelationshipManager,
    BimService,
    ProjectBimManager,
)

__all__ = [
    "BIM_SCHEMA_VERSION",
    "BimAdapter",
    "BimAdapterRegistry",
    "BimCategory",
    "BimDocument",
    "BimDocumentRepository",
    "BimElement",
    "BimEvent",
    "BimEventDispatcher",
    "BimEventName",
    "BimParameterManager",
    "BimParameterSet",
    "BimRelationship",
    "BimRelationshipManager",
    "BimService",
    "ProjectBimManager",
    "RelationshipType",
    "create_default_bim_adapter_registry",
]
