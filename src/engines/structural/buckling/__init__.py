from dataclasses import dataclass
from math import pi

@dataclass(frozen=True, slots=True)
class BucklingMode:
    mode_number: int
    load_factor: float
    def __post_init__(self):
        if self.mode_number < 1 or self.load_factor <= 0:
            raise ValueError("Datos inválidos")

class LinearBucklingEngine:
    def euler_load(self, elastic_modulus, inertia, effective_length):
        if min(elastic_modulus, inertia, effective_length) <= 0:
            raise ValueError("Valores positivos requeridos")
        return pi**2 * elastic_modulus * inertia / effective_length**2
    def critical_mode(self, modes):
        if not modes:
            raise ValueError("modes no puede estar vacío")
        return min(modes, key=lambda m: m.load_factor)
