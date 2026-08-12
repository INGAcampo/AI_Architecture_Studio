from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WallJoinKind(str, Enum):
    L = "L"
    T = "T"
    X = "X"
    BUTT = "butt"
    MITER = "miter"


@dataclass(frozen=True, slots=True)
class WallJoin:
    join_id: str
    wall_ids: tuple[str, ...]
    kind: WallJoinKind
    cleaned: bool = False

    def __post_init__(self) -> None:
        if not self.join_id.strip():
            raise ValueError("join_id no puede estar vacío")
        if len(self.wall_ids) < 2:
            raise ValueError("Un join requiere al menos dos muros")
        if len(set(self.wall_ids)) != len(self.wall_ids):
            raise ValueError("Los wall_ids deben ser únicos")


class WallJoinEngine:
    def __init__(self) -> None:
        self._joins: dict[str, WallJoin] = {}

    def create(self, join: WallJoin) -> WallJoin:
        if join.join_id in self._joins:
            raise KeyError(f"Join ya existente: {join.join_id}")
        self._joins[join.join_id] = join
        return join

    def get(self, join_id: str) -> WallJoin:
        try:
            return self._joins[join_id]
        except KeyError as exc:
            raise KeyError(f"Join desconocido: {join_id}") from exc

    def clean(self, join_id: str) -> WallJoin:
        join = self.get(join_id)
        cleaned = WallJoin(join.join_id, join.wall_ids, join.kind, True)
        self._joins[join_id] = cleaned
        return cleaned

    def for_wall(self, wall_id: str) -> tuple[WallJoin, ...]:
        return tuple(join for join in self._joins.values() if wall_id in join.wall_ids)
