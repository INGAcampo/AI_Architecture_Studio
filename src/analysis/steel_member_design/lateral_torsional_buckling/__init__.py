class LateralTorsionalBucklingEngine:
    def nominal_moment_nmm(self, mp_nmm, lb_mm, lp_mm, lr_mm, mr_nmm):
        if lb_mm <= lp_mm: return mp_nmm
        if lb_mm >= lr_mm: return mr_nmm
        return mp_nmm - (mp_nmm-mr_nmm)*(lb_mm-lp_mm)/(lr_mm-lp_mm)
