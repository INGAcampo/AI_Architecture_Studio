"""Point and window selection over CAD entity extents."""
from __future__ import annotations
from .geometry import BoundingBox

class SelectionEngine:
    """Resolve entities intersecting pick tolerances or selection windows."""
    def window(self, entities, box: BoundingBox):
        """Execute the public SelectionEngine.window operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return tuple(e for e in entities if box.contains_box(e.bbox()))

    def crossing(self, entities, box: BoundingBox):
        """Execute the public SelectionEngine.crossing operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return tuple(e for e in entities if box.intersects(e.bbox()))

    def by_layer(self, entities, layer: str):
        """Execute the public SelectionEngine.by_layer operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return tuple(e for e in entities if e.layer == layer)

    def by_type(self, entities, entity_type):
        """Execute the public SelectionEngine.by_type operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return tuple(e for e in entities if isinstance(e, entity_type))
