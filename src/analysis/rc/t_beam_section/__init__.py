from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class TBeamSection: web_width:float; flange_width:float; flange_thickness:float; depth:float; effective_depth:float
