from __future__ import annotations

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterDefinition,
    ParameterType,
)
from engines.regeneration import RegenerationItem


def roof_parameter_definitions():
    return (
        ParameterDefinition("elevation", "Elevación", ParameterType.LENGTH, unit="m", default_value=0.0),
        ParameterDefinition("pitch_degrees", "Pendiente", ParameterType.ANGLE, unit="deg", minimum=0.0, maximum=89.999, default_value=0.0),
        ParameterDefinition("overhang", "Voladizo", ParameterType.LENGTH, unit="m", minimum=0.0, default_value=0.0),
        ParameterDefinition("projected_area", "Área proyectada", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("sloped_area", "Área inclinada", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("volume", "Volumen", ParameterType.VOLUME, unit="m³", access=ParameterAccess.CALCULATED, default_value=0.0),
    )


class RoofRegenerationAdapter:
    def __init__(self, roof_engine, regeneration_engine) -> None:
        self.roof_engine = roof_engine
        self.regeneration_engine = regeneration_engine

    def register_roof(self, roof_id: str) -> RegenerationItem:
        item = RegenerationItem(
            object_id=f"roof:{roof_id}",
            callback=lambda: self.roof_engine.calculate_quantities(roof_id),
            priority=45,
        )
        self.regeneration_engine.register(item)
        return item
