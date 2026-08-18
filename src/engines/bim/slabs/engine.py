from __future__ import annotations

from typing import Any

from .catalog import SlabTypeCatalog
from .model import IntelligentSlab, SlabOpening, SlabType
from .quantities import SlabQuantityCalculator
from .validation import SlabValidator


class IntelligentSlabEngine:
    def __init__(self, *, event_dispatcher=None) -> None:
        self.catalog = SlabTypeCatalog()
        self.validator = SlabValidator()
        self.quantities = SlabQuantityCalculator()
        self.event_dispatcher = event_dispatcher
        self._slabs: dict[str, IntelligentSlab] = {}

    def register_type(self, slab_type: SlabType) -> None:
        self.catalog.register(slab_type)
        self._publish("slab.type.registered", type_id=slab_type.type_id)

    def add_slab(self, slab: IntelligentSlab) -> IntelligentSlab:
        if slab.slab_id in self._slabs:
            raise KeyError(f"Losa ya existente: {slab.slab_id}")
        self.catalog.get(slab.slab_type_id)
        result = self.validator.validate(slab)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._slabs[slab.slab_id] = slab
        self._publish("slab.added", slab_id=slab.slab_id)
        return slab

    def get_slab(self, slab_id: str) -> IntelligentSlab:
        try:
            return self._slabs[slab_id]
        except KeyError as exc:
            raise KeyError(f"Losa desconocida: {slab_id}") from exc

    def remove_slab(self, slab_id: str) -> IntelligentSlab:
        slab = self.get_slab(slab_id)
        self._slabs.pop(slab_id)
        self._publish("slab.removed", slab_id=slab_id)
        return slab

    def change_type(self, slab_id: str, type_id: str) -> IntelligentSlab:
        self.catalog.get(type_id)
        slab = self.get_slab(slab_id)
        if slab.slab_type_id != type_id:
            slab.slab_type_id = type_id
            slab.touch()
            self._publish("slab.type.changed", slab_id=slab_id, type_id=type_id)
        return slab

    def add_opening(self, slab_id: str, opening: SlabOpening) -> IntelligentSlab:
        slab = self.get_slab(slab_id)
        if any(item.opening_id == opening.opening_id for item in slab.openings):
            raise KeyError(f"Hueco ya existente: {opening.opening_id}")
        previous = slab.openings
        slab.openings = slab.openings + (opening,)
        result = self.validator.validate(slab)
        if not result.valid:
            slab.openings = previous
            raise ValueError("; ".join(result.errors))
        slab.touch()
        self._publish("slab.opening.added", slab_id=slab_id, opening_id=opening.opening_id)
        return slab

    def remove_opening(self, slab_id: str, opening_id: str) -> IntelligentSlab:
        slab = self.get_slab(slab_id)
        filtered = tuple(item for item in slab.openings if item.opening_id != opening_id)
        if len(filtered) == len(slab.openings):
            raise KeyError(f"Hueco desconocido: {opening_id}")
        slab.openings = filtered
        slab.touch()
        self._publish("slab.opening.removed", slab_id=slab_id, opening_id=opening_id)
        return slab

    def set_slope(self, slab_id: str, slope: float, direction_degrees: float) -> IntelligentSlab:
        if slope < 0:
            raise ValueError("slope no puede ser negativa")
        slab = self.get_slab(slab_id)
        slab.slope = float(slope)
        slab.slope_direction_degrees = float(direction_degrees)
        slab.touch()
        self._publish(
            "slab.slope.changed",
            slab_id=slab_id,
            slope=slab.slope,
            direction_degrees=slab.slope_direction_degrees,
        )
        return slab

    def calculate_quantities(self, slab_id: str):
        slab = self.get_slab(slab_id)
        slab_type = self.catalog.get(slab.slab_type_id)
        return self.quantities.calculate(slab, slab_type)

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
