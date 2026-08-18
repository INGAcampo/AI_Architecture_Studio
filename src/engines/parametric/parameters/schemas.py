from __future__ import annotations

from .types import (
    ParameterAccess,
    ParameterDefinition,
    ParameterScope,
    ParameterType,
)


def wall_parameter_schema() -> tuple[ParameterDefinition, ...]:
    return (
        ParameterDefinition(
            "name",
            "Nombre",
            ParameterType.STRING,
            group="Identidad",
            default_value="Muro",
        ),
        ParameterDefinition(
            "height",
            "Altura",
            ParameterType.LENGTH,
            group="Dimensiones",
            unit="m",
            minimum=0.01,
            default_value=3.0,
        ),
        ParameterDefinition(
            "thickness",
            "Espesor",
            ParameterType.LENGTH,
            group="Dimensiones",
            unit="m",
            minimum=0.001,
            default_value=0.20,
        ),
        ParameterDefinition(
            "base_elevation",
            "Elevación base",
            ParameterType.LENGTH,
            group="Restricciones",
            unit="m",
            default_value=0.0,
        ),
        ParameterDefinition(
            "phase",
            "Fase",
            ParameterType.ENUM,
            group="Construcción",
            enum_values=("Existing", "Demolition", "New Construction", "Future"),
            default_value="New Construction",
        ),
        ParameterDefinition(
            "structural",
            "Estructural",
            ParameterType.BOOLEAN,
            group="Construcción",
            default_value=False,
        ),
        ParameterDefinition(
            "material_id",
            "Material",
            ParameterType.MATERIAL,
            group="Materiales",
            default_value="",
        ),
        ParameterDefinition(
            "area",
            "Área",
            ParameterType.AREA,
            group="Cantidades",
            access=ParameterAccess.CALCULATED,
            unit="m²",
            default_value=0.0,
        ),
        ParameterDefinition(
            "volume",
            "Volumen",
            ParameterType.VOLUME,
            group="Cantidades",
            access=ParameterAccess.CALCULATED,
            unit="m³",
            default_value=0.0,
        ),
        ParameterDefinition(
            "type_mark",
            "Marca de tipo",
            ParameterType.STRING,
            group="Identidad",
            scope=ParameterScope.TYPE,
            default_value="",
        ),
    )
