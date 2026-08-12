from dataclasses import dataclass
from math import pi, sqrt, exp

@dataclass(frozen=True, slots=True)
class CompressionBucklingResult:
    elastic_buckling_stress: float
    critical_stress: float
    nominal_capacity: float
    design_capacity: float
    inelastic: bool

class CompressionBucklingEngine:
    def calculate(self, profile, material, slenderness, phi=0.9):
        if slenderness <= 0:
            raise ValueError("Esbeltez inválida")
        fe=(pi*pi*material.elastic_modulus)/(slenderness*slenderness)
        limit=4.71*sqrt(material.elastic_modulus/material.fy)
        if slenderness<=limit:
            fcr=(0.658**(material.fy/fe))*material.fy
            inelastic=True
        else:
            fcr=0.877*fe
            inelastic=False
        pn=fcr*profile.area
        return CompressionBucklingResult(fe,fcr,pn,phi*pn,inelastic)
