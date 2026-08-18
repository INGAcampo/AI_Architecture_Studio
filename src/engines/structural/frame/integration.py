from __future__ import annotations

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterDefinition,
    ParameterType,
)
from engines.regeneration import RegenerationItem


def structural_member_parameter_definitions():
    return (
        ParameterDefinition("length", "Longitud", ParameterType.LENGTH, unit="m", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("rotation", "Rotación", ParameterType.ANGLE, unit="deg", default_value=0.0),
        ParameterDefinition("area", "Área de sección", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("volume", "Volumen", ParameterType.VOLUME, unit="m³", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("mass", "Masa", ParameterType.FLOAT, access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("weight", "Peso", ParameterType.FLOAT, access=ParameterAccess.CALCULATED, default_value=0.0),
    )


class StructuralFrameRegenerationAdapter:
    def __init__(self, frame_engine, regeneration_engine) -> None:
        self.frame_engine = frame_engine
        self.regeneration_engine = regeneration_engine

    def register_member(self, member_id: str) -> RegenerationItem:
        item = RegenerationItem(
            object_id=f"structural:{member_id}",
            callback=lambda: self.frame_engine.calculate_quantities(member_id),
            priority=35,
        )
        self.regeneration_engine.register(item)
        return item
