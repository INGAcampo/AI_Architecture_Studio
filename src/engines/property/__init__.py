"""Motor de propiedades tipadas de AI Architecture Studio."""

from .definition import PropertyDefinition
from .exceptions import (
    DuplicatePropertyError,
    PropertyError,
    PropertyNotFoundError,
    PropertyReadOnlyError,
    PropertyValidationError,
    UnitConversionError,
)
from .groups import PropertyGroup
from .registry import PropertyRegistry
from .serializer import PropertySerializer
from .service import PropertyService
from .types import PropertyType
from .units import UnitConverter, UnitDefinition, UnitRegistry
from .validators import (
    AllowedValuesValidator,
    CompositeValidator,
    LengthValidator,
    RangeValidator,
    RequiredValidator,
)
from .value import PropertyValue

__all__ = [
    "AllowedValuesValidator",
    "CompositeValidator",
    "DuplicatePropertyError",
    "LengthValidator",
    "PropertyDefinition",
    "PropertyError",
    "PropertyGroup",
    "PropertyNotFoundError",
    "PropertyReadOnlyError",
    "PropertyRegistry",
    "PropertySerializer",
    "PropertyService",
    "PropertyType",
    "PropertyValidationError",
    "PropertyValue",
    "RangeValidator",
    "RequiredValidator",
    "UnitConversionError",
    "UnitConverter",
    "UnitDefinition",
    "UnitRegistry",
]

from .parameter_binding import ParameterBinding
from .parameter_catalog import StandardParameterCatalog
from .parameter_library import SharedParameterLibrary
from .shared_parameter import (
    IfcMapping,
    ParameterDiscipline,
    ParameterScope,
    SharedParameter,
)

__all__ += [
    "IfcMapping",
    "ParameterBinding",
    "ParameterDiscipline",
    "ParameterScope",
    "SharedParameter",
    "SharedParameterLibrary",
    "StandardParameterCatalog",
]
