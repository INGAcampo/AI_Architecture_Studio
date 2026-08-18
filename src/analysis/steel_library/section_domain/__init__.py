from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SteelSection:
    designation:str; family:str; area_mm2:float; mass_kg_m:float; ix_mm4:float; iy_mm4:float; j_mm4:float=0.; cw_mm6:float=0.; depth_mm:float=0.; width_mm:float=0.
    @property
    def rx_mm(self): return (self.ix_mm4/self.area_mm2)**.5
    @property
    def ry_mm(self): return (self.iy_mm4/self.area_mm2)**.5
