"""Catálogo inicial de parámetros BIM reutilizables."""

from __future__ import annotations

from .definition import PropertyDefinition
from .groups import PropertyGroup
from .parameter_binding import ParameterBinding
from .parameter_library import SharedParameterLibrary
from .shared_parameter import (
    IfcMapping,
    ParameterDiscipline,
    ParameterScope,
    SharedParameter,
)
from .types import PropertyType
from .validators import RangeValidator


class StandardParameterCatalog:
    @staticmethod
    def create() -> SharedParameterLibrary:
        library = SharedParameterLibrary("AIAS Standard Parameter Catalog")

        parameters = (
            SharedParameter(
                guid="aias-common-manufacturer-v1",
                discipline=ParameterDiscipline.COMMON,
                definition=PropertyDefinition(
                    "Manufacturer",
                    PropertyType.TEXT,
                    display_name="Fabricante",
                    group=PropertyGroup.IDENTITY,
                ),
            ),
            SharedParameter(
                guid="aias-common-model-v1",
                discipline=ParameterDiscipline.COMMON,
                definition=PropertyDefinition(
                    "Model",
                    PropertyType.TEXT,
                    display_name="Modelo",
                    group=PropertyGroup.IDENTITY,
                ),
            ),
            SharedParameter(
                guid="aias-architecture-fire-rating-v1",
                discipline=ParameterDiscipline.ARCHITECTURE,
                definition=PropertyDefinition(
                    "FireRating",
                    PropertyType.TEXT,
                    display_name="Resistencia al fuego",
                    group=PropertyGroup.IDENTITY,
                ),
                ifc_mapping=IfcMapping(
                    "Pset_WallCommon",
                    "FireRating",
                ),
            ),
            SharedParameter(
                guid="aias-architecture-thermal-resistance-v1",
                discipline=ParameterDiscipline.ARCHITECTURE,
                definition=PropertyDefinition(
                    "ThermalResistance",
                    PropertyType.DECIMAL,
                    display_name="Resistencia térmica",
                    group=PropertyGroup.ENERGY,
                    validators=(RangeValidator(minimum=0.0),),
                ),
            ),
            SharedParameter(
                guid="aias-structural-concrete-strength-v1",
                discipline=ParameterDiscipline.STRUCTURAL,
                definition=PropertyDefinition(
                    "ConcreteStrength",
                    PropertyType.PRESSURE,
                    display_name="Resistencia del concreto",
                    group=PropertyGroup.STRUCTURAL,
                    unit="MPa",
                    validators=(RangeValidator(minimum=0.0),),
                ),
            ),
            SharedParameter(
                guid="aias-mep-flow-v1",
                discipline=ParameterDiscipline.MEP,
                definition=PropertyDefinition(
                    "Flow",
                    PropertyType.DECIMAL,
                    display_name="Caudal",
                    group=PropertyGroup.MEP,
                ),
            ),
            SharedParameter(
                guid="aias-cost-unit-cost-v1",
                discipline=ParameterDiscipline.COST,
                definition=PropertyDefinition(
                    "UnitCost",
                    PropertyType.DECIMAL,
                    display_name="Costo unitario",
                    group=PropertyGroup.COST,
                    validators=(RangeValidator(minimum=0.0),),
                ),
            ),
        )

        for parameter in parameters:
            library.register(parameter)

        library.add_binding(
            ParameterBinding(
                "aias-architecture-fire-rating-v1",
                scope=ParameterScope.CATEGORY,
                categories=("Wall", "Door"),
            )
        )
        library.add_binding(
            ParameterBinding(
                "aias-architecture-thermal-resistance-v1",
                scope=ParameterScope.CATEGORY,
                categories=("Wall", "Roof", "Slab"),
            )
        )
        library.add_binding(
            ParameterBinding(
                "aias-structural-concrete-strength-v1",
                scope=ParameterScope.CATEGORY,
                categories=("Beam", "Column", "Foundation", "Slab"),
            )
        )
        return library
