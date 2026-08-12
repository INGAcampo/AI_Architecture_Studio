"""Registro y conversión dimensional sin dependencias externas."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import UnitConversionError


@dataclass(frozen=True)
class UnitDefinition:
    symbol: str
    dimension: str
    scale_to_si: float = 1.0
    offset_to_si: float = 0.0

    def to_si(self, value: float) -> float:
        return float(value) * self.scale_to_si + self.offset_to_si

    def from_si(self, value: float) -> float:
        return (float(value) - self.offset_to_si) / self.scale_to_si


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, UnitDefinition] = {}

    def register(self, definition: UnitDefinition, *aliases: str) -> None:
        keys = (definition.symbol, *aliases)
        for key in keys:
            normalized = self._normalize(key)
            self._units[normalized] = definition

    def get(self, symbol: str) -> UnitDefinition:
        try:
            return self._units[self._normalize(symbol)]
        except KeyError as error:
            raise UnitConversionError(
                f"Unidad no registrada: {symbol!r}."
            ) from error

    def contains(self, symbol: str) -> bool:
        return self._normalize(symbol) in self._units

    @staticmethod
    def _normalize(symbol: str) -> str:
        return str(symbol).strip().lower()

    @classmethod
    def create_default(cls) -> "UnitRegistry":
        registry = cls()

        definitions = (
            (UnitDefinition("m", "length"), ("meter", "metre")),
            (UnitDefinition("cm", "length", 0.01), ()),
            (UnitDefinition("mm", "length", 0.001), ()),
            (UnitDefinition("ft", "length", 0.3048), ("foot", "feet")),
            (UnitDefinition("in", "length", 0.0254), ("inch",)),
            (UnitDefinition("m²", "area"), ("m2",)),
            (UnitDefinition("ft²", "area", 0.09290304), ("ft2",)),
            (UnitDefinition("m³", "volume"), ("m3",)),
            (UnitDefinition("ft³", "volume", 0.028316846592), ("ft3",)),
            (UnitDefinition("deg", "angle"), ("°", "degree")),
            (UnitDefinition("rad", "angle", 57.29577951308232), ()),
            (UnitDefinition("N", "force"), ("newton",)),
            (UnitDefinition("kN", "force", 1000.0), ()),
            (UnitDefinition("lbf", "force", 4.4482216152605), ()),
            (UnitDefinition("Pa", "pressure"), ("pascal",)),
            (UnitDefinition("kPa", "pressure", 1000.0), ()),
            (UnitDefinition("MPa", "pressure", 1_000_000.0), ()),
            (UnitDefinition("psi", "pressure", 6894.757293168), ()),
            (UnitDefinition("K", "temperature"), ("kelvin",)),
            (UnitDefinition("°C", "temperature", 1.0, 273.15), ("c", "celsius")),
            (
                UnitDefinition(
                    "°F",
                    "temperature",
                    5.0 / 9.0,
                    255.3722222222222,
                ),
                ("f", "fahrenheit"),
            ),
        )
        for definition, aliases in definitions:
            registry.register(definition, *aliases)
        return registry


class UnitConverter:
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        self.registry = registry or UnitRegistry.create_default()

    def convert(
        self,
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:
        source = self.registry.get(from_unit)
        target = self.registry.get(to_unit)
        if source.dimension != target.dimension:
            raise UnitConversionError(
                f"No se puede convertir {source.dimension!r} "
                f"a {target.dimension!r}."
            )
        return target.from_si(source.to_si(float(value)))
