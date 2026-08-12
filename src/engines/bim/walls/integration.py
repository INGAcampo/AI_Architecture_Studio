from __future__ import annotations

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterDefinition,
    ParameterType,
)
from engines.regeneration import RegenerationItem


def wall_parameter_definitions():
    return (
        ParameterDefinition("length", "Longitud", ParameterType.LENGTH, unit="m", minimum=0.01, default_value=1.0),
        ParameterDefinition("height", "Altura", ParameterType.LENGTH, unit="m", minimum=0.01, default_value=3.0),
        ParameterDefinition("base_elevation", "Elevación base", ParameterType.LENGTH, unit="m", default_value=0.0),
        ParameterDefinition("top_elevation", "Elevación superior", ParameterType.LENGTH, unit="m", access=ParameterAccess.CALCULATED, default_value=3.0),
        ParameterDefinition("gross_area", "Área bruta", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("net_area", "Área neta", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("volume", "Volumen", ParameterType.VOLUME, unit="m³", access=ParameterAccess.CALCULATED, default_value=0.0),
    )


class WallRegenerationAdapter:
    def __init__(self, wall_engine, regeneration_engine) -> None:
        self.wall_engine = wall_engine
        self.regeneration_engine = regeneration_engine

    def register_wall(self, wall_id: str) -> RegenerationItem:
        item = RegenerationItem(
            object_id=f"wall:{wall_id}",
            callback=lambda: self.wall_engine.calculate_quantities(wall_id),
            priority=30,
        )
        self.regeneration_engine.register(item)
        return item
