class TensionGrossYieldEngine:
    def nominal_strength_n(self, area_mm2, fy_mpa):
        return area_mm2 * fy_mpa
