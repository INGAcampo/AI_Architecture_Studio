class BeamDeflectionEngine:
    def simply_supported_uniform_mm(self, w_n_per_mm, length_mm, e_mpa, i_mm4):
        return 5*w_n_per_mm*length_mm**4/(384*e_mpa*i_mm4)
