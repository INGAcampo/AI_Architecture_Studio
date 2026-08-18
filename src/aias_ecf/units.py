"""Dimension-safe engineering-unit definitions and SI-based conversion."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UnitDefinition:
    """Unit symbol, physical dimension and multiplicative conversion to SI."""
    symbol: str
    dimension: str
    to_si: float

class UnitsEngine:
    """Convert supported units while rejecting cross-dimension operations."""
    UNITS = {
        "m": UnitDefinition("m","length",1.0),
        "cm": UnitDefinition("cm","length",0.01),
        "mm": UnitDefinition("mm","length",0.001),
        "ft": UnitDefinition("ft","length",0.3048),
        "in": UnitDefinition("in","length",0.0254),
        "N": UnitDefinition("N","force",1.0),
        "kN": UnitDefinition("kN","force",1000.0),
        "lbf": UnitDefinition("lbf","force",4.4482216152605),
        "Pa": UnitDefinition("Pa","pressure",1.0),
        "kPa": UnitDefinition("kPa","pressure",1000.0),
        "MPa": UnitDefinition("MPa","pressure",1_000_000.0),
        "psi": UnitDefinition("psi","pressure",6894.757293168),
        "kg": UnitDefinition("kg","mass",1.0),
        "g": UnitDefinition("g","mass",0.001),
        "s": UnitDefinition("s","time",1.0),
        "min": UnitDefinition("min","time",60.0),
        "h": UnitDefinition("h","time",3600.0),
    }

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert through SI factors while requiring matching physical dimensions."""
        src = self.UNITS[from_unit]
        dst = self.UNITS[to_unit]
        if src.dimension != dst.dimension:
            raise ValueError("dimension_mismatch")
        return value * src.to_si / dst.to_si

    def compatible(self, unit_a: str, unit_b: str) -> bool:
        """Return whether two registered units share the same dimension."""
        return self.UNITS[unit_a].dimension == self.UNITS[unit_b].dimension
