from .catalog import SlabTypeCatalog
from .engine import IntelligentSlabEngine
from .geometry import is_clockwise, point_in_polygon, polygon_area, polygon_perimeter
from .integration import SlabRegenerationAdapter, slab_parameter_definitions
from .model import (
    IntelligentSlab,
    Point2D,
    SlabKind,
    SlabLayer,
    SlabLayerFunction,
    SlabOpening,
    SlabStructure,
    SlabType,
)
from .quantities import SlabQuantities, SlabQuantityCalculator
from .validation import SlabValidationResult, SlabValidator

__all__ = [
    "IntelligentSlab",
    "IntelligentSlabEngine",
    "Point2D",
    "SlabKind",
    "SlabLayer",
    "SlabLayerFunction",
    "SlabOpening",
    "SlabQuantities",
    "SlabQuantityCalculator",
    "SlabRegenerationAdapter",
    "SlabStructure",
    "SlabType",
    "SlabTypeCatalog",
    "SlabValidationResult",
    "SlabValidator",
    "is_clockwise",
    "point_in_polygon",
    "polygon_area",
    "polygon_perimeter",
    "slab_parameter_definitions",
]
