from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SteelMaterial:
    name:str; standard:str; fy_mpa:float; fu_mpa:float; e_mpa:float=200000.; poisson:float=.30; density_kg_m3:float=7850.; alpha_per_c:float=1.2e-5
    @property
    def shear_modulus_mpa(self): return self.e_mpa/(2*(1+self.poisson))
