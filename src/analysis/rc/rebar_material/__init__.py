from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RebarMaterial: name:str; fy:float; elastic_modulus:float=200000
