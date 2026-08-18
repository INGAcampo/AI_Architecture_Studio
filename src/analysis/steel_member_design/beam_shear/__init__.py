class BeamShearEngine:
    def nominal_strength_n(self, fy_mpa, web_area_mm2, cv=1.0):
        return 0.6 * fy_mpa * web_area_mm2 * cv
