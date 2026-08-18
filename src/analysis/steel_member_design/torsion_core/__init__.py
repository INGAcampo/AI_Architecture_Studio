class TorsionEngine:
    def shear_stress_mpa(self, torque_nmm, radius_mm, j_mm4):
        return torque_nmm*radius_mm/max(j_mm4,1e-12)
