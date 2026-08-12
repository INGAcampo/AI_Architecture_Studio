from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DesignFactors:
    phi_tension: float = 0.90
    phi_compression: float = 0.90
    phi_flexure: float = 0.90
    phi_shear: float = 1.00
    omega_tension: float = 1.67
    omega_compression: float = 1.67
    omega_flexure: float = 1.67
    omega_shear: float = 1.50
