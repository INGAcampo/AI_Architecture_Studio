class TensionNetRuptureEngine:
    def nominal_strength_n(self, net_area_mm2, fu_mpa, shear_lag=1.0):
        return net_area_mm2 * fu_mpa * shear_lag
