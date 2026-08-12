"""Canonical foundation and footprint-shape classifications."""
from enum import Enum

class FoundationType(str, Enum):
    """Supported shallow-foundation engineering-object families."""
    ISOLATED = "ISOLATED"
    COMBINED = "COMBINED"
    STRIP = "STRIP"
    MAT = "MAT"
    PEDESTAL = "PEDESTAL"
    FOUNDATION_BEAM = "FOUNDATION_BEAM"

class ShapeType(str, Enum):
    """Supported plan-shape representations for foundation geometry."""
    RECTANGULAR = "RECTANGULAR"
    SQUARE = "SQUARE"
    CIRCULAR = "CIRCULAR"
