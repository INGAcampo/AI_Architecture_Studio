import math
class BeamVibrationEngine:
    def first_frequency_hz(self, stiffness_n_per_m, mass_kg):
        return (1/(2*math.pi))*math.sqrt(stiffness_n_per_m/max(mass_kg,1e-12))
