from __future__ import annotations


class Foundation:
    """Foundation model with compatible dimensions and derived geometry."""

    ISOLATED = "isolated"
    COMBINED = "combined"
    MAT = "mat"

    def __init__(
        self,
        width: float = 0.0,
        length: float = 0.0,
        thickness: float = 0.0,
        **properties,
    ):
        self.name = properties.pop("name", "Fundación")
        self.level = properties.pop("level", "Cimentación")
        self.foundation_type = properties.pop("foundation_type", self.ISOLATED)
        self.material = properties.pop("material", "Concreto armado")
        self.concrete_strength_mpa = float(properties.pop("concrete_strength_mpa", 25.0))
        self.soil_bearing_capacity_kpa = float(properties.pop("soil_bearing_capacity_kpa", 150.0))
        self.foundation_depth_m = float(properties.pop("foundation_depth_m", 1.50))
        self.design_code = properties.pop("design_code", "")
        self.unit_system = properties.pop("unit_system", "metric_decimal")
        self.density_kg_m3 = float(properties.pop("density_kg_m3", 2400.0))

        self.width = self._positive(width, "width")
        self.length = self._positive(length, "length")
        self.thickness = self._positive(thickness, "thickness")
        self.area = self.width * self.length
        self.volume = self.area * self.thickness

        self.properties = dict(properties.pop("properties", {}))
        self.properties.update(properties)

    @staticmethod
    def _positive(value: float, name: str) -> float:
        number = float(value)
        if number < 0.0:
            raise ValueError(f"{name} cannot be negative.")
        return number
