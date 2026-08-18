from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConcreteMaterial:
    name:str; fc:float; density:float=2400
    def elastic_modulus(self): return 4700*self.fc**.5
