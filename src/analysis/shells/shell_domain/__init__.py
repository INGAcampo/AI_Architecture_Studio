from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ShellLayer: material_id:str; thickness:float; angle_deg:float
