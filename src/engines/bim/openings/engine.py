from __future__ import annotations

from dataclasses import replace
from typing import Any

from .collision import OpeningCollisionDetector
from .model import HostWallGeometry, Opening, OpeningPlacement, OpeningState
from .quantities import OpeningQuantityCalculator
from .relationships import OpeningRelationshipManager
from .validation import OpeningValidator


class IntelligentOpeningEngine:
    def __init__(self, *, event_dispatcher=None) -> None:
        self.relationships = OpeningRelationshipManager()
        self.validator = OpeningValidator()
        self.quantities = OpeningQuantityCalculator()
        self.collisions = OpeningCollisionDetector()
        self._walls: dict[str, HostWallGeometry] = {}
        self.event_dispatcher = event_dispatcher

    def register_wall(self, wall: HostWallGeometry, *, replace_existing: bool = False) -> None:
        if wall.wall_id in self._walls and not replace_existing:
            raise KeyError(f"Muro ya registrado: {wall.wall_id}")
        self._walls[wall.wall_id] = wall
        self._publish("opening.wall.registered", wall_id=wall.wall_id)

    def update_wall(self, wall: HostWallGeometry) -> None:
        if wall.wall_id not in self._walls:
            raise KeyError(f"Muro desconocido: {wall.wall_id}")
        previous = self._walls[wall.wall_id]
        self._walls[wall.wall_id] = wall
        self._reposition_relative(previous, wall)
        self._publish("opening.wall.updated", wall_id=wall.wall_id)

    def add_opening(self, opening: Opening) -> Opening:
        wall = self.require_wall(opening.host_wall_id)
        result = self.validator.validate(opening, wall)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self.relationships.attach(opening)
        collisions = self.collisions.detect(self.relationships.for_wall(wall.wall_id))
        if collisions:
            self.relationships.detach(opening.opening_id)
            raise ValueError("El hueco colisiona con otro hueco")
        self._publish(
            "opening.added",
            opening_id=opening.opening_id,
            wall_id=opening.host_wall_id,
            kind=opening.kind.value,
        )
        return opening

    def remove_opening(self, opening_id: str) -> Opening:
        opening = self.relationships.detach(opening_id)
        self._publish("opening.removed", opening_id=opening_id)
        return opening

    def resize(self, opening_id: str, width: float, height: float) -> Opening:
        opening = self.relationships.get(opening_id)
        previous = (opening.width, opening.height)
        opening.width = float(width)
        opening.height = float(height)
        opening.touch()
        try:
            self._validate_and_check(opening)
        except Exception:
            opening.width, opening.height = previous
            opening.touch()
            raise
        self._publish(
            "opening.resized",
            opening_id=opening_id,
            width=opening.width,
            height=opening.height,
        )
        return opening

    def move(
        self,
        opening_id: str,
        *,
        offset: float | None = None,
        sill_height: float | None = None,
    ) -> Opening:
        opening = self.relationships.get(opening_id)
        previous = opening.placement
        opening.placement = OpeningPlacement(
            previous.offset if offset is None else float(offset),
            previous.sill_height if sill_height is None else float(sill_height),
            previous.flip_horizontal,
            previous.flip_vertical,
        )
        opening.touch()
        try:
            self._validate_and_check(opening)
        except Exception:
            opening.placement = previous
            opening.touch()
            raise
        self._publish(
            "opening.moved",
            opening_id=opening_id,
            offset=opening.placement.offset,
            sill_height=opening.placement.sill_height,
        )
        return opening

    def suppress(self, opening_id: str, suppressed: bool = True) -> Opening:
        opening = self.relationships.get(opening_id)
        opening.state = OpeningState.SUPPRESSED if suppressed else OpeningState.ACTIVE
        opening.touch()
        self._publish(
            "opening.suppression.changed",
            opening_id=opening_id,
            suppressed=suppressed,
        )
        return opening

    def wall_quantities(self, wall_id: str):
        wall = self.require_wall(wall_id)
        openings = tuple(
            opening
            for opening in self.relationships.for_wall(wall_id)
            if opening.state is OpeningState.ACTIVE
        )
        return self.quantities.calculate(wall, openings)

    def require_wall(self, wall_id: str) -> HostWallGeometry:
        try:
            return self._walls[wall_id]
        except KeyError as exc:
            raise KeyError(f"Muro desconocido: {wall_id}") from exc

    def _validate_and_check(self, opening: Opening) -> None:
        wall = self.require_wall(opening.host_wall_id)
        result = self.validator.validate(opening, wall)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        collisions = [
            collision
            for collision in self.collisions.detect(self.relationships.for_wall(wall.wall_id))
            if opening.opening_id in {collision.first_id, collision.second_id}
        ]
        if collisions:
            raise ValueError("El hueco colisiona con otro hueco")

    def _reposition_relative(
        self,
        previous: HostWallGeometry,
        current: HostWallGeometry,
    ) -> None:
        scale = current.length / previous.length
        for opening in self.relationships.for_wall(current.wall_id):
            ratio = opening.placement.offset / previous.length
            opening.placement = replace(
                opening.placement,
                offset=ratio * current.length,
            )
            opening.touch()
            result = self.validator.validate(opening, current)
            if not result.valid:
                opening.state = OpeningState.ORPHANED

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
