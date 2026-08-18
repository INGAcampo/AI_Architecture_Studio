from __future__ import annotations
from .scene import CadScene

class CadDiagnostics:
    def inspect(self, scene: CadScene) -> dict:
        entities = scene.all()
        return {
            "entity_count": len(entities),
            "layers": len(scene.layers.names()),
            "visible_entities": sum(1 for entity in entities if entity.visible),
            "locked_entities": sum(1 for entity in entities if entity.locked),
            "status": "PASS",
        }
