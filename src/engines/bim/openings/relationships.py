from __future__ import annotations

from collections import defaultdict

from .model import Opening


class OpeningRelationshipManager:
    def __init__(self) -> None:
        self._by_wall: dict[str, set[str]] = defaultdict(set)
        self._openings: dict[str, Opening] = {}
        self.revision = 0

    def attach(self, opening: Opening, *, replace: bool = False) -> None:
        existing = self._openings.get(opening.opening_id)
        if existing is not None and not replace:
            raise KeyError(f"Hueco ya registrado: {opening.opening_id}")

        if existing is not None:
            self._by_wall[existing.host_wall_id].discard(existing.opening_id)

        self._openings[opening.opening_id] = opening
        self._by_wall[opening.host_wall_id].add(opening.opening_id)
        self.revision += 1

    def detach(self, opening_id: str) -> Opening:
        opening = self.get(opening_id)
        self._openings.pop(opening_id)
        self._by_wall[opening.host_wall_id].discard(opening_id)
        self.revision += 1
        return opening

    def get(self, opening_id: str) -> Opening:
        try:
            return self._openings[opening_id]
        except KeyError as exc:
            raise KeyError(f"Hueco desconocido: {opening_id}") from exc

    def for_wall(self, wall_id: str) -> tuple[Opening, ...]:
        return tuple(
            sorted(
                (self._openings[opening_id] for opening_id in self._by_wall.get(wall_id, set())),
                key=lambda opening: (opening.placement.offset, opening.opening_id),
            )
        )

    def move_to_wall(self, opening_id: str, new_wall_id: str) -> Opening:
        opening = self.get(opening_id)
        if opening.host_wall_id == new_wall_id:
            return opening
        self._by_wall[opening.host_wall_id].discard(opening_id)
        opening.host_wall_id = new_wall_id
        opening.touch()
        self._by_wall[new_wall_id].add(opening_id)
        self.revision += 1
        return opening

    def all(self) -> tuple[Opening, ...]:
        return tuple(self._openings[key] for key in sorted(self._openings))
