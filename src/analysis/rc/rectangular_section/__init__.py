from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RectangularSection:
    width:float; depth:float; effective_depth:float
    def gross_inertia(self): return self.width*self.depth**3/12
