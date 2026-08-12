"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UnitDefinition:
    """Execute the public UnitDefinition operation for the Omega application core and shared runtime services using explicit caller inputs."""
    symbol: str
    to_si: float

class UnitSystem:
    """Execute the public UnitSystem operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._units = {
            "m": UnitDefinition("m", 1.0),
            "mm": UnitDefinition("mm", 0.001),
            "cm": UnitDefinition("cm", 0.01),
            "in": UnitDefinition("in", 0.0254),
            "ft": UnitDefinition("ft", 0.3048),
            "N": UnitDefinition("N", 1.0),
            "kN": UnitDefinition("kN", 1000.0),
            "Pa": UnitDefinition("Pa", 1.0),
            "MPa": UnitDefinition("MPa", 1_000_000.0),
        }

    def convert(self, value: float, source: str, target: str) -> float:
        """Execute the public UnitSystem.convert operation for the Omega application core and shared runtime services using explicit caller inputs."""
        if source not in self._units or target not in self._units:
            raise KeyError(source if source not in self._units else target)
        si = value * self._units[source].to_si
        return si / self._units[target].to_si
