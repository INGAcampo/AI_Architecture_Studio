from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class MaterialState: stress:tuple;plastic_strain:tuple;equivalent_plastic_strain:float;damage:float;yielded:bool
