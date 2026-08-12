"""Elastic Euler column-buckling reference calculations."""
from math import pi

class EulerBuckling:
    """Compute critical axial load from stiffness, length and effective-length factor."""
    def critical_load(self, elastic_modulus_pa, inertia_m4, length_m, k_factor=1.0):
        """Execute the public EulerBuckling.critical_load operation for the Omega structural analysis and design suite using explicit caller inputs."""
        if min(elastic_modulus_pa,inertia_m4,length_m,k_factor) <= 0:
            raise ValueError("Invalid buckling input.")
        return pi*pi*elastic_modulus_pa*inertia_m4/(k_factor*length_m)**2
