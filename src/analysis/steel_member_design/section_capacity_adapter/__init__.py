class SectionCapacityAdapter:
    def plastic_modulus_mm3(self, section):
        return getattr(section, "zx_mm3", section.ix_mm4/max(section.depth_mm/2,1e-12))
