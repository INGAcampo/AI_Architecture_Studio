from dataclasses import dataclass
from math import pi, sqrt

@dataclass(frozen=True, slots=True)
class ModalMode:
    mode_number: int
    eigenvalue: float
    participation_factor: float = 0.0
    def __post_init__(self):
        if self.mode_number < 1 or self.eigenvalue <= 0:
            raise ValueError("Datos modales inválidos")
    @property
    def circular_frequency(self):
        return sqrt(self.eigenvalue)
    @property
    def frequency_hz(self):
        return self.circular_frequency / (2*pi)
    @property
    def period(self):
        return 1.0 / self.frequency_hz

class ModalAnalysisFoundation:
    def sort_modes(self, modes):
        return tuple(sorted(modes, key=lambda m: m.eigenvalue))
    def cumulative_participation(self, modes):
        return sum(m.participation_factor for m in modes)
