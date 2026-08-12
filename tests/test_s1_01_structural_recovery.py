from __future__ import annotations

from engines.structural import BeamAnalysis, ColumnAnalysis, FoundationAnalysis
from models.structural import Beam, Column, Foundation


def test_structural_packages_are_importable() -> None:
    assert BeamAnalysis is not None
    assert ColumnAnalysis is not None
    assert FoundationAnalysis is not None


def test_beam_geometry_compatibility() -> None:
    beam = Beam(start_point=(0.0, 0.0), end_point=(3.0, 4.0))
    assert beam.length == 5.0


def test_column_geometry_compatibility() -> None:
    column = Column(width=0.40, depth=0.40, height=3.00)
    assert round(column.volume, 2) == 0.48


def test_foundation_geometry_compatibility() -> None:
    foundation = Foundation(width=2.0, length=2.0, thickness=0.5)
    assert foundation.area == 4.0
    assert foundation.volume == 2.0
