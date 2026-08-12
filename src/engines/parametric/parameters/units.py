from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UnitDefinition:
    symbol: str
    dimension: str
    to_si: float


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, UnitDefinition] = {}
        self.register(UnitDefinition("m", "length", 1.0))
        self.register(UnitDefinition("cm", "length", 0.01))
        self.register(UnitDefinition("mm", "length", 0.001))
        self.register(UnitDefinition("ft", "length", 0.3048))
        self.register(UnitDefinition("in", "length", 0.0254))
        self.register(UnitDefinition("m²", "area", 1.0))
        self.register(UnitDefinition("cm²", "area", 0.0001))
        self.register(UnitDefinition("m³", "volume", 1.0))
        self.register(UnitDefinition("L", "volume", 0.001))
        self.register(UnitDefinition("deg", "angle", 1.0))
        self.register(UnitDefinition("rad", "angle", 57.29577951308232))

    def register(self, unit: UnitDefinition, *, replace: bool = False) -> None:
        if unit.symbol in self._units and not replace:
            raise KeyError(f"Unidad ya registrada: {unit.symbol}")
        if unit.to_si <= 0:
            raise ValueError("to_si debe ser positivo")
        self._units[unit.symbol] = unit

    def get(self, symbol: str) -> UnitDefinition:
        try:
            return self._units[symbol]
        except KeyError as exc:
            raise KeyError(f"Unidad desconocida: {symbol}") from exc

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        source = self.get(from_unit)
        target = self.get(to_unit)
        if source.dimension != target.dimension:
            raise ValueError("No se pueden convertir dimensiones diferentes")
        return float(value) * source.to_si / target.to_si

    def symbols(self, dimension: str | None = None) -> tuple[str, ...]:
        items = self._units.values()
        if dimension is not None:
            items = [unit for unit in items if unit.dimension == dimension]
        return tuple(sorted(unit.symbol for unit in items))
