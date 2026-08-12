from __future__ import annotations

from typing import Any

from .catalog import RoofTypeCatalog
from .model import IntelligentRoof, RoofOpening, RoofType
from .quantities import RoofQuantityCalculator
from .validation import RoofValidator


class IntelligentRoofEngine:
    def __init__(self, *, event_dispatcher=None) -> None:
        self.catalog = RoofTypeCatalog()
        self.validator = RoofValidator()
        self.quantities = RoofQuantityCalculator()
        self.event_dispatcher = event_dispatcher
        self._roofs: dict[str, IntelligentRoof] = {}

    def register_type(self, roof_type: RoofType) -> None:
        self.catalog.register(roof_type)
        self._publish("roof.type.registered", type_id=roof_type.type_id)

    def add_roof(self, roof: IntelligentRoof) -> IntelligentRoof:
        if roof.roof_id in self._roofs:
            raise KeyError(f"Cubierta ya existente: {roof.roof_id}")
        self.catalog.get(roof.roof_type_id)
        result = self.validator.validate(roof)
        if not result.valid:
            raise ValueError("; ".join(result.errors))
        self._roofs[roof.roof_id] = roof
        self._publish("roof.added", roof_id=roof.roof_id)
        return roof

    def get_roof(self, roof_id: str) -> IntelligentRoof:
        try:
            return self._roofs[roof_id]
        except KeyError as exc:
            raise KeyError(f"Cubierta desconocida: {roof_id}") from exc

    def remove_roof(self, roof_id: str) -> IntelligentRoof:
        roof = self.get_roof(roof_id)
        self._roofs.pop(roof_id)
        self._publish("roof.removed", roof_id=roof_id)
        return roof

    def change_type(self, roof_id: str, type_id: str) -> IntelligentRoof:
        self.catalog.get(type_id)
        roof = self.get_roof(roof_id)
        if roof.roof_type_id != type_id:
            roof.roof_type_id = type_id
            roof.touch()
            self._publish("roof.type.changed", roof_id=roof_id, type_id=type_id)
        return roof

    def set_pitch(self, roof_id: str, pitch_degrees: float) -> IntelligentRoof:
        if not 0 <= pitch_degrees < 90:
            raise ValueError("pitch_degrees debe estar entre 0 y 90")
        roof = self.get_roof(roof_id)
        roof.pitch_degrees = float(pitch_degrees)
        roof.touch()
        self._publish("roof.pitch.changed", roof_id=roof_id, pitch_degrees=roof.pitch_degrees)
        return roof

    def set_overhang(self, roof_id: str, overhang: float) -> IntelligentRoof:
        if overhang < 0:
            raise ValueError("overhang no puede ser negativo")
        roof = self.get_roof(roof_id)
        roof.overhang = float(overhang)
        roof.touch()
        self._publish("roof.overhang.changed", roof_id=roof_id, overhang=roof.overhang)
        return roof

    def add_opening(self, roof_id: str, opening: RoofOpening) -> IntelligentRoof:
        roof = self.get_roof(roof_id)
        if any(item.opening_id == opening.opening_id for item in roof.openings):
            raise KeyError(f"Hueco ya existente: {opening.opening_id}")
        previous = roof.openings
        roof.openings = roof.openings + (opening,)
        result = self.validator.validate(roof)
        if not result.valid:
            roof.openings = previous
            raise ValueError("; ".join(result.errors))
        roof.touch()
        return roof

    def remove_opening(self, roof_id: str, opening_id: str) -> IntelligentRoof:
        roof = self.get_roof(roof_id)
        filtered = tuple(item for item in roof.openings if item.opening_id != opening_id)
        if len(filtered) == len(roof.openings):
            raise KeyError(f"Hueco desconocido: {opening_id}")
        roof.openings = filtered
        roof.touch()
        return roof

    def calculate_quantities(self, roof_id: str):
        roof = self.get_roof(roof_id)
        roof_type = self.catalog.get(roof.roof_type_id)
        return self.quantities.calculate(roof, roof_type)

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
