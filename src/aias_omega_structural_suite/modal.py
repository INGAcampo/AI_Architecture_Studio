"""Simplified shear-building modal frequency solver."""
from math import sqrt

class ShearBuildingModalSolver:
    """Estimate vibration modes from story mass and lateral stiffness arrays."""
    def solve_two_story(self, k1, k2, m1, m2):
        """Execute the public ShearBuildingModalSolver.solve_two_story operation for the Omega structural analysis and design suite using explicit caller inputs."""
        if min(k1,k2,m1,m2) <= 0:
            raise ValueError("Positive stiffnesses and masses required.")
        a = m1*m2
        b = -(k1*m2 + k2*m1 + k2*m2)
        c = k1*k2
        disc = b*b - 4*a*c
        l1 = (-b - disc**0.5)/(2*a)
        l2 = (-b + disc**0.5)/(2*a)
        return tuple(sorted((sqrt(l1), sqrt(l2))))
