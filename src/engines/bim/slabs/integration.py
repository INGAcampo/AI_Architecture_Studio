from __future__ import annotations

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterDefinition,
    ParameterType,
)
from engines.regeneration import RegenerationItem


def slab_parameter_definitions():
    return (
        ParameterDefinition("elevation", "Elevación", ParameterType.LENGTH, unit="m", default_value=0.0),
        ParameterDefinition("slope", "Pendiente", ParameterType.FLOAT, minimum=0.0, default_value=0.0),
        ParameterDefinition("gross_area", "Área bruta", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("opening_area", "Área de huecos", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("net_area", "Área neta", ParameterType.AREA, unit="m²", access=ParameterAccess.CALCULATED, default_value=0.0),
        ParameterDefinition("volume", "Volumen", ParameterType.VOLUME, unit="m³", access=ParameterAccess.CALCULATED, default_value=0.0),
    )


class SlabRegenerationAdapter:
    def __init__(self, slab_engine, regeneration_engine) -> None:
        self.slab_engine = slab_engine
        self.regeneration_engine = regeneration_engine

    def register_slab(self, slab_id: str) -> RegenerationItem:
        item = RegenerationItem(
            object_id=f"slab:{slab_id}",
            callback=lambda: self.slab_engine.calculate_quantities(slab_id),
            priority=40,
        )
        self.regeneration_engine.register(item)
        return item
