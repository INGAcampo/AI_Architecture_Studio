from .catalog import RoofTypeCatalog
from .engine import IntelligentRoofEngine
from .geometry import point_in_polygon, polygon_area, polygon_perimeter, sloped_area
from .integration import RoofRegenerationAdapter, roof_parameter_definitions
from .model import (
    IntelligentRoof,
    RoofKind,
    RoofLayer,
    RoofLayerFunction,
    RoofOpening,
    RoofPoint,
    RoofStructure,
    RoofType,
)
from .quantities import RoofQuantities, RoofQuantityCalculator
from .validation import RoofValidationResult, RoofValidator

__all__ = [
    "IntelligentRoof",
    "IntelligentRoofEngine",
    "RoofKind",
    "RoofLayer",
    "RoofLayerFunction",
    "RoofOpening",
    "RoofPoint",
    "RoofQuantities",
    "RoofQuantityCalculator",
    "RoofRegenerationAdapter",
    "RoofStructure",
    "RoofType",
    "RoofTypeCatalog",
    "RoofValidationResult",
    "RoofValidator",
    "point_in_polygon",
    "polygon_area",
    "polygon_perimeter",
    "roof_parameter_definitions",
    "sloped_area",
]
