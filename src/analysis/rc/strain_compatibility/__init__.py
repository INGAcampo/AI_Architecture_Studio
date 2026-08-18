class StrainCompatibilityEngine:
    def steel_strain(self,c,d,ecu=.003): return ecu*(d-c)/max(c,1e-12)
