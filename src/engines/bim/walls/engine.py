from __future__ import annotations

from dataclasses import replace
from typing import Any

from .catalog import WallTypeCatalog
from .joins import WallJoin, WallJoinEngine
from .model import IntelligentWall, WallLocationLine, WallType
from .quantities import WallQuantityCalculator


class IntelligentWallEngine:
    def __init__(self, *, event_dispatcher=None, opening_engine=None) -> None:
        self.catalog = WallTypeCatalog()
        self.joins = WallJoinEngine()
        self.quantities = WallQuantityCalculator()
        self.opening_engine = opening_engine
        self.event_dispatcher = event_dispatcher
        self._walls: dict[str, IntelligentWall] = {}

    def register_type(self, wall_type: WallType) -> None:
        self.catalog.register(wall_type)
        self._publish("wall.type.registered", type_id=wall_type.type_id)

    def add_wall(self, wall: IntelligentWall) -> IntelligentWall:
        if wall.wall_id in self._walls:
            raise KeyError(f"Muro ya existente: {wall.wall_id}")
        self.catalog.get(wall.wall_type_id)
        self._walls[wall.wall_id] = wall
        self._publish("wall.added", wall_id=wall.wall_id)
        return wall

    def get_wall(self, wall_id: str) -> IntelligentWall:
        try:
            return self._walls[wall_id]
        except KeyError as exc:
            raise KeyError(f"Muro desconocido: {wall_id}") from exc

    def remove_wall(self, wall_id: str) -> IntelligentWall:
        wall = self.get_wall(wall_id)
        self._walls.pop(wall_id)
        self._publish("wall.removed", wall_id=wall_id)
        return wall

    def change_type(self, wall_id: str, type_id: str) -> IntelligentWall:
        self.catalog.get(type_id)
        wall = self.get_wall(wall_id)
        if wall.wall_type_id != type_id:
            wall.wall_type_id = type_id
            wall.touch()
            self._publish("wall.type.changed", wall_id=wall_id, type_id=type_id)
        return wall

    def resize(self, wall_id: str, *, length: float | None = None, height: float | None = None) -> IntelligentWall:
        wall = self.get_wall(wall_id)
        if length is not None:
            if length <= 0:
                raise ValueError("length debe ser positiva")
            wall.length = float(length)
        if height is not None:
            if height <= 0:
                raise ValueError("height debe ser positiva")
            wall.height = float(height)
        wall.touch()
        self._publish("wall.resized", wall_id=wall_id, length=wall.length, height=wall.height)
        return wall

    def set_location_line(self, wall_id: str, location_line: WallLocationLine) -> IntelligentWall:
        wall = self.get_wall(wall_id)
        wall.location_line = location_line
        wall.touch()
        return wall

    def flip(self, wall_id: str) -> IntelligentWall:
        wall = self.get_wall(wall_id)
        wall.flipped = not wall.flipped
        wall.touch()
        self._publish("wall.flipped", wall_id=wall_id, flipped=wall.flipped)
        return wall

    def create_join(self, join: WallJoin) -> WallJoin:
        for wall_id in join.wall_ids:
            self.get_wall(wall_id)
        created = self.joins.create(join)
        self._publish("wall.join.created", join_id=join.join_id)
        return created

    def clean_join(self, join_id: str) -> WallJoin:
        cleaned = self.joins.clean(join_id)
        self._publish("wall.join.cleaned", join_id=join_id)
        return cleaned

    def calculate_quantities(self, wall_id: str):
        wall = self.get_wall(wall_id)
        wall_type = self.catalog.get(wall.wall_type_id)
        opening_area = 0.0
        if self.opening_engine is not None:
            try:
                opening_area = self.opening_engine.wall_quantities(wall_id).opening_area
            except KeyError:
                opening_area = 0.0
        return self.quantities.calculate(wall, wall_type, opening_area=opening_area)

    def _publish(self, name: str, **payload: Any) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
