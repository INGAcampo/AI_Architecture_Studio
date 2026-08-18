"""AIAS Shadow Structural Platform."""
from .contracts import (
    BeamSection,
    LoadCase,
    LoadCombination,
    Material,
    PointLoad,
    SimplySupportedBeam,
    UniformLoad,
)
from .solver import BeamResult, solve_simply_supported_beam

__all__ = [
    "BeamSection",
    "LoadCase",
    "LoadCombination",
    "Material",
    "PointLoad",
    "SimplySupportedBeam",
    "UniformLoad",
    "BeamResult",
    "solve_simply_supported_beam",
]
