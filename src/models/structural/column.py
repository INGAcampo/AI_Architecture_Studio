from __future__ import annotations


class Column:
    """Structural column model with automatic volume calculation."""

    RECTANGULAR = "rectangular"
    CIRCULAR = "circular"

    def __init__(
        self,
        width: float = 0.30,
        depth: float = 0.30,
        height: float = 3.00,
        **properties,
    ):
        self.name = properties.pop("name", "Columna")
        self.level = properties.pop("level", "Nivel 1")
        self.material = properties.pop("material", "Concreto armado")
        self.concrete_strength_mpa = float(properties.pop("concrete_strength_mpa", 25.0))
        self.steel_grade = properties.pop("steel_grade", "Fy 420 MPa")
        self.cover_cm = float(properties.pop("cover_cm", 4.0))
        self.design_code = properties.pop("design_code", "")
        self.unit_system = properties.pop("unit_system", "metric_decimal")
        self.density_kg_m3 = float(properties.pop("density_kg_m3", 2400.0))

        self.width = self._positive(width, "width")
        self.depth = self._positive(depth, "depth")
        self.height = self._positive(height, "height")
        self.volume = self.width * self.depth * self.height

        self.properties = dict(properties.pop("properties", {}))
        self.properties.update(properties)

    @staticmethod
    def _positive(value: float, name: str) -> float:
        number = float(value)
        if number < 0.0:
            raise ValueError(f"{name} cannot be negative.")
        return number
