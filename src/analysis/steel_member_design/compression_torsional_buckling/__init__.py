class TorsionalBucklingEngine:
    def critical_stress_mpa(self, e_mpa, g_mpa, cw_mm6, j_mm4, ix_mm4, iy_mm4, length_mm):
        numerator = (3.141592653589793**2 * e_mpa * cw_mm6 / max(length_mm**2,1e-12)) + g_mpa*j_mm4
        return numerator / max(ix_mm4 + iy_mm4, 1e-12)
