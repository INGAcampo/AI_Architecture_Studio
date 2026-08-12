from __future__ import annotations

from engines.regeneration import RegenerationItem

from .engine import IntelligentOpeningEngine


class OpeningRegenerationAdapter:
    def __init__(self, opening_engine: IntelligentOpeningEngine, regeneration_engine) -> None:
        self.opening_engine = opening_engine
        self.regeneration_engine = regeneration_engine

    def register_wall(self, wall_id: str) -> RegenerationItem:
        item = RegenerationItem(
            object_id=f"openings:{wall_id}",
            callback=lambda: self.opening_engine.wall_quantities(wall_id),
            priority=50,
            dependencies=(wall_id,),
        )
        self.regeneration_engine.register(item)
        return item

    def invalidate_wall(self, wall_id: str) -> None:
        self.regeneration_engine.mark_dirty(f"openings:{wall_id}")
